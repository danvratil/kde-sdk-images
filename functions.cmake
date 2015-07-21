##
#
# Copyright 2015  Daniel Vrátil <dvratil@redhat.com>
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License as
# published by the Free Software Foundation; either version 2 of
# the License or (at your option) version 3 or any later version
# accepted by the membership of KDE e.V. (or its successor approved
# by the membership of KDE e.V.), which shall act as a proxy
# defined in Section 14 of version 3 of the license.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##


######## Custom Macros #########
function(createSDK name version snap)
    set(sdkname "${name}-sdk-${version}")
    add_custom_command(
        OUTPUT ${sdkname}.tar.gz ${sdkname}-rpmdb.tar.gz
        COMMAND ${CMAKE_SOURCE_DIR}/setup.sh ${SDK_BASE_IMAGE}
        COMMAND ${CMAKE_SOURCE_DIR}/build.sh smart install -y ${NOARCH}/${sdkname}-${snap}.sdk.noarch.rpm
        COMMAND ${CMAKE_COMMAND} -E remove -f ${sdkname}.tar.gz ${sdkname}-rpmdb.tar.gz
        COMMAND tar --transform "s,^build/root/usr,files,S" -czf ${sdkname}.tar.gz build/root/usr --owner=root
        COMMAND tar --transform "s,^build/var,files,S" -czf ${sdkname}-rpmdb.tar.gz build/var/lib/rpm --owner=root
        COMMAND ${CMAKE_COMMAND} -E cmake_echo_color --green \"* Cleaning up build root ...\"
        COMMAND ${CMAKE_COMMAND} -E remove_directory ${CMAKE_SOURCE_DIR}/build/root
        COMMAND ${CMAKE_COMMAND} -E remove_directory ${CMAKE_SOURCE_DIR}/build/var
        COMMAND ${CMAKE_COMMAND} -E cmake_echo_color --green \"* Done\"
        DEPENDS ${${sdkname}_target} ${SDK_BASE_IMAGE}
        VERBATIM
    )
endfunction()

function(createPlatform name version packages)
    set(installablePkgs)
    foreach (package ${packages})
        set(exclude "FALSE")
        foreach (match IN ITEMS "-dev-" "-debuginfo-" "-sdk-" "-static-" "-bootstrap-")
            STRING(FIND "${package}" "${match}" pos REVERSE)
            if (${pos} GREATER -1)
                set(exclude "TRUE")
            endif()
        endforeach()
        if ("${exclude}" STREQUAL "FALSE")
            LIST(APPEND installablePkgs ${package})
        endif()
        unset(exclude)
    endforeach()
    #STRING(REPLACE ";" " " installablePkgs ${installablePkgs})
    #message(STATUS ${installablePkgs})
    set(platformname "${name}-platform-${version}")
    add_custom_command(
        OUTPUT ${platformname}.tar.gz ${platformname}-rpmdb.tar.gz
        COMMAND ${CMAKE_COMMAND} -E cmake_echo_color --cyan "Building ${platformname}"
        COMMAND ${CMAKE_SOURCE_DIR}/setup_root.sh ${PLATFORM_BASE_IMAGE} > /dev/null
        COMMAND ${CMAKE_SOURCE_DIR}/build.sh rpm -Uvh --nodeps ${installablePkgs}
        COMMAND tar --transform "s,^build/root/usr,files,S" -czf ${platformname}.tar.gz build/root/usr --owner=root > /dev/null
        COMMAND tar --transform "s,^build/var,files,S" -czf ${platformname}-rpmdb.tar.gz build/var/lib/rpm --owner=root > /dev/null
        COMMAND ${CMAKE_COMMAND} -E cmake_echo_color --green \"* Cleaning up build root ...\"
        COMMAND ${CMAKE_COMMAND} -E remove_directory ${CMAKE_SOURCE_DIR}/build/root
        COMMAND ${CMAKE_COMMAND} -E remove_directory ${CMAKE_SOURCE_DIR}/build/var
        COMMAND ${CMAKE_COMMAND} -E cmake_echo_color --green \"* Done\"
        DEPENDS ${${platformname}_target} ${PLATFORM_BASE_IMAGE}
    )
endfunction()

function(parseSPECFile package specFile sourcesList depsList)
    execute_process(COMMAND ${CMAKE_COMMAND} -E echo_append "-- Parsing SPEC file for package ${package}")
    # The path must be relative - we use it as both target name and actual file path,
    # but absolute paths differ here and in chroot in build.sh
    execute_process(COMMAND rpmspec -D "_topdir ${CMAKE_SOURCE_DIR}/packages" -D "dist .sdk" -q ${specFile} --qf "%{NAME}=packages/RPMS/%{ARCH}/%{NAME}-%{VERSION}-%{RELEASE}.%{ARCH}.rpm;"
                    OUTPUT_VARIABLE rawProvidesList)
    execute_process(COMMAND rpmspec -D "_topdir ${CMAKE_SOURCE_DIR}/packages" -D "dist .sdk" -q ${specFile} --buildrequires
                    OUTPUT_VARIABLE rawBuildRequiresList)
#    execute_process(COMMAND rpmspec -D "_topdir ${CMAKE_SOURCE_DIR}/packages" -D "dist .sdk" -q ${specFile} --requires
#                    OUTPUT_VARIABLE rawRequiresList)
    execute_process(COMMAND rpmspec -D "_topdir ${CMAKE_SOURCE_DIR}/packages" -D "dist .sdk" -P ${specFile}
                    OUTPUT_VARIABLE parsedFile)

    foreach(provides ${rawProvidesList})
        STRING(REGEX MATCH "^([0-9a-zA-Z_-]+)=(.*)$" match ${provides})
        set(${CMAKE_MATCH_1}_target ${CMAKE_MATCH_2})
        set(${CMAKE_MATCH_1}_target ${CMAKE_MATCH_2} PARENT_SCOPE)
        LIST(APPEND ${package}_targets ${CMAKE_MATCH_1})
    endforeach()

    STRING(REGEX REPLACE ";" "\\\\;" rawBuildRequiresList "${rawBuildRequiresList}")
    STRING(REGEX REPLACE "\n" ";" buildRequiresList "${rawBuildRequiresList}")
    LIST(APPEND ${depsList} ${buildRequiresList})

#    STRING(REGEX REPLACE ";" "\\\\;" rawRequiresList "${rawRequiresList}")
#    STRING(REGEX REPLACE "\n" ";" requiresList "${rawRequiresList}")
#    LIST(APPEND ${depsList} ${requiresList})

    STRING(REGEX REPLACE ";" "\\\\;" parsedFile "${parsedFile}")
    STRING(REGEX REPLACE "\n" ";" parsedFile "${parsedFile}")
    foreach(line ${parsedFile})
        STRING(REGEX MATCHALL "^Source[0-9]*:(.*)$" matches "${line}")
        if (NOT "${CMAKE_MATCH_1}" STREQUAL "")
            STRING(STRIP "${CMAKE_MATCH_1}" urlStripped)
            if (${urlStripped} MATCHES "^(http|https|ftp):.*$")
                LIST(APPEND ${sourcesList} "${urlStripped}")
            endif()
        endif()
    endforeach()

    set(${package}_targets ${${package}_targets} PARENT_SCOPE)
    set(sourcesList ${sourcesList} PARENT_SCOPE)
    set(${depsList} ${${depsList}} PARENT_SCOPE)

    execute_process(COMMAND ${CMAKE_COMMAND} -E echo " -- done")
endfunction()

function(generatePackageTargets platform packages allTargets)
    if (NOT EXISTS "${CMAKE_SOURCE_DIR}/packages/SOURCES")
        FILE(MAKE_DIRECTORY "${CMAKE_SOURCE_DIR}/packages/SOURCES")
    endif()

    foreach(package ${packages})
        set(specFile "${CMAKE_SOURCE_DIR}/packages/SPECS/${platform}/${package}.spec")
        if (NOT EXISTS "${specFile}")
            message(FATAL_ERROR "SPEC file for package ${package} does not exist: ${specFile}")
        endif()

        parseSPECFile(${package} ${specFile} ${package}_sources ${package}_deps)

        set(${package}_targets ${${package}_targets} PARENT_SCOPE)
        set(${package}_sources ${${package}_sources} PARENT_SCOPE)
        set(${package}_deps ${${package}_deps} PARENT_SCOPE)
        foreach(tgt ${${package}_targets})
            set(${tgt}_target ${${tgt}_target} PARENT_SCOPE)
        endforeach()
    endforeach()

    # Generate targets for each package:
    # ${package} (meta target)
    #  '-- ${package}-build (build)
    #       '-- ${package}-sources (get sources)
    set(allDestFiles "")
    foreach(package ${packages})
        add_custom_target("${platform}-${package}")

        # Use relative path to SPEC file, because absolute paths differ here and in the build.sh chroot
        set(specFile "packages/SPECS/${platform}/${package}.spec")

        # List of local source tarballs
        set(sourceFiles "")
        foreach(source ${${package}_sources})
            get_filename_component(fileName ${source} NAME)
            set(destFile "${CMAKE_SOURCE_DIR}/packages/SOURCES/${fileName}")
            LIST(APPEND sourceFiles ${destFile})
            LIST(FIND allDestFiles ${destFile} found)
            if (${found} EQUAL -1)
                LIST(APPEND allDestFiles ${destFile})
                add_custom_command(
                    OUTPUT ${destFile}
                    COMMAND ${CMAKE_COMMAND} -E cmake_echo_color --cyan \"Downloading source for ${package}\"
                    COMMAND if [ -e ${destFile} ]; then echo \"${destFile} already exists\"\; else wget ${source} -O ${destFile}\; fi
                    DEPENDS ${specFile}
                )
            endif()
        endforeach()
        if ("${sourceFiles}")
            # Only create the ${package}-source target if there are any sources
            add_custom_target(${platform}-${package}-sources
                DEPENDS ${destFiles}
            )
            add_dependencies(${platform}-${package} ${platform}-${package}-sources)
        endif()

        set(depsPackages "")
        foreach(dep ${${package}_deps})
            LIST(APPEND depsPackages ${${dep}_target})
        endforeach()
        if (depsPackages)
            # smart does not like duplicates
            LIST(REMOVE_DUPLICATES depsPackages)
            set(installDeps ${CMAKE_SOURCE_DIR}/build.sh smart install -y ${depsPackages})
        else()
            set(installDeps true)
            set(depTargets "")
        endif()
        set(targets "")
        foreach(tgt ${${package}_targets})
            LIST(APPEND targets ${${tgt}_target})
            LIST(APPEND ${allTargets} ${${tgt}_target})
        endforeach()

        add_custom_command(
            OUTPUT ${targets}
            COMMAND ${CMAKE_COMMAND} -E cmake_echo_color --cyan \"Building ${package}\"
            COMMAND ${CMAKE_COMMAND} -E cmake_echo_color --green \"* Preparing build root ...\"
            COMMAND ${CMAKE_SOURCE_DIR}/setup.sh ${SDK_BASE_IMAGE}
            COMMAND ${CMAKE_COMMAND} -E cmake_echo_color --green \"* Installing dependencies ...\"
            COMMAND ${installDeps}
            COMMAND ${CMAKE_COMMAND} -E cmake_echo_color --green \"* Building ...\"
            COMMAND ${CMAKE_SOURCE_DIR}/build.sh rpmbuild --clean -bb ${specFile} | tee packages/LOGS/${package}.build
            COMMAND ${CMAKE_COMMAND} -E cmake_echo_color --green \"* Cleaning up build root ...\"
            COMMAND ${CMAKE_COMMAND} -E remove_directory ${CMAKE_SOURCE_DIR}/build/root
            COMMAND ${CMAKE_COMMAND} -E remove_directory ${CMAKE_SOURCE_DIR}/build/var
            COMMAND ${CMAKE_COMMAND} -E cmake_echo_color --green \"* Done\"
            DEPENDS ${SDK_BASE_IMAGE} ${PLATFORM_BASE_IMAGE} ${specFile} ${sourceFiles} ${depsPackages}
        )
        add_custom_target(${platform}-${package}-build
            DEPENDS ${targets}
        )
        add_dependencies(${platform}-${package} ${platform}-${package}-build)

    endforeach()
    unset(allDestFiles)

    set(${allTargets} ${${allTargets}} PARENT_SCOPE)
endfunction()

function(createBaseImages)
    add_custom_command(OUTPUT ${CMAKE_SOURCE_DIR}/freedesktop-sdk-base/Makefile
                       COMMAND ${CMAKE_COMMAND} -E cmake_echo_color --cyan "Cloning freedesktop-sdk-base"
                       COMMAND git clone git://git.gnome.org/freedesktop-sdk-base
                       COMMAND cd freedesktop-sdk-base && git fetch origin
                       COMMAND cd freedesktop-sdk-base && git checkout ${BASE_HASH}
                       WORKING_DIRECTORY ${CMAKE_SOURCE_DIR}
    )

    # FIXME: Hardcoded -j5
    add_custom_command(OUTPUT ${SDK_BASE_IMAGE} ${PLATFORM_BASE_IMAGE}
                       COMMAND make -j5
                       WORKING_DIRECTORY ${CMAKE_SOURCE_DIR}/freedesktop-sdk-base
                       DEPENDS "${CMAKE_SOURCE_DIR}/freedesktop-sdk-base/Makefile"
    )

endfunction()

function(commit name version)
    function(_commit type uri name version)
        add_custom_command(OUTPUT ${uri}-${version}.repo
                           COMMAND if [ ! -d repo ]\; then ostree init --mode=archive-z2 --repo=repo else \"Using existing repo\"\; fi
                           COMMAND ${CMAKE_SOURCE_DIR}/commit.sh repo ${name}-${type}-${version}.tar.gz ${name}-${type}-${version}-rpmdb.tar.gz ${uri}.${version}.metadata ${uri} ${BUILD_ARCH} ${version}
                           COMMAND ${CMAKE_COMMAND} -E touch ${CMAKE_SOURCE_DIR}/${uri}-${version}.repo
                           DEPENDS ${name}-${type}-${version}.tar.gz ${name}-${type}-${version}-rpmdb.tar.gz
        )
    endfunction()

    STRING(TOLOWER ${name} lcname)
    _commit(platform org.kde.${name}.Platform ${lcname} ${version})
    _commit(sdk org.kde.${name}.Sdk ${lcname} ${version})
endfunction()

function(untag name version)
    function(_untag type uri version)
        add_custom_command(OUTPUT ${uri}.repo.untagged
                           COMMAND ${CMAKE_SOURCE_DIR}/untag.sh repo ${uri} ${BUILD_ARCH} ${version}
                           COMMAND ${CMAKE_COMMAND} -E touch ${CMAKE_SOURCE_DIR}/${uri}.repo.untagged
                           DEPENDS ${uri}.repo
        )
    endfunction()

    STRING(TOLOWER ${name} lcname)
    _untag(platform org.kde.${name}.Platform ${version})
    _untag(sdk org.kde.${name}.Sdk ${version})
endfunction()