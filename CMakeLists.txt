project(kde-sdk-images)
cmake_minimum_required(VERSION 3.0)

set(FREEDESKTOP_VERSION "1.0")
set(QT5_VERSION "5.4.1")
set(KF5_VERSION "5.9.0")
set(BUILD_ARCH "x86_64")
set(BASE_HASH "8e44c998adbf1546c45cf733c688fed74e8ddc89")
set(NOARCH "packages/RPMS/noarch")

set(IMAGE_DIR "${CMAKE_SOURCE_DIR}/freedesktop-sdk-base/images/${BUILD_ARCH}")

set(SDK_BASE_IMAGE "${IMAGE_DIR}/freedesktop-contents-sdk-${BUILD_ARCH}-${BASE_HASH}.tar.gz")
set(PLATFORM_BASE_IMAGE "${IMAGE_DIR}/freedesktop-contents-platform-${BUILD_ARCH}-${BASE_HASH}.tar.gz")

set(freedesktop_PACKAGES
    freedesktop-platform-base
    freedesktop-platform
    freedesktop-sdk-base
    freedesktop-sdk

    abattis-cantarell-fonts
    aspell
    atk
    cairo
    dbus-glib
    dbus
    dejavu-fonts
    desktop-file-utils
    fontconfig
    freetype
    gdk-pixbuf2
    glib2
    gnu-free-fonts
    gobject-introspection
    google-crosextra-caladea-fonts
    google-crosextra-carlito-fonts
    graphite2
    gstreamer1-plugins-base
    gstreamer1
    gtk-doc-stub
    gtk2
    harfbuzz
    hicolor-icon-theme
    hunspell
    hunspell-en
    libdatrie
    libdrm
    libepoxy
    liberation-fonts
    libICE
    libpciaccess
    libproxy
    libSM
    libthai
    libX11
    libXau
    libxcb
    libXcomposite
    libXcursor
    libXdamage
    libXdmcp
    libXext
    libXfixes
    libXft
    libXinerama
    libXi
    libxkbcommon
    libXpm
    libXrandr
    libXrender
    libXScrnSaver
    libxshmfence
    libXt
    libXtst
    libXv
    libXxf86vm
    llvm
    mesa
    orc
    pango
    pixman
    pulseaudio
    SDL2
    SDL2_image
    SDL2_mixer
    SDL2_net
    SDL2_ttf
    shared-mime-info
    wayland
    xcb-proto
    xkeyboard-config
    xorg-x11-proto-devel
    xorg-x11-util-macros
    xorg-x11-xtrans-devel
)


######## Custom Macros #########
macro(createSDK name)
    set(sdkname "${name}-sdk")
    add_custom_command(
        OUTPUT ${sdkname}.tar.gz ${sdkname}-rpmdb.tar.gz
        COMMAND ${CMAKE_CURRENT_SOURCE_DIR}/setup.sh ${SDK_BASE_IMAGE} > /dev/null
        COMMAND ${CMAKE_CURRENT_SOURCE_DIR}/build.sh smart install -y ${NOARCH}/${sdkname}-0.1-1.sdk.noarch.rpm
        COMMAND ${CMAKE_COMMAND} -E remove -f ${sdkname}.tar.gz ${sdkname}-rpmdb.tar.gz
        COMMAND tar --transform "s,^build/root/usr,files,S" -czf ${sdkname}.tar.gz build/root/usr --owner=root > /dev/null
        COMMAND tar --transform "s,^build/var,files,S" -czf ${sdkname}-rpmdb.tar.gz build/var/lib/rpm --owner=root > /dev/null
        COMMAND ${CMAKE_CURRENT_SOURCE_DIR}/clear_root.sh
        DEPENDS ${${sdkname}_target} ${SDK_BASE_IMAGE}
        VERBATIM
    )
endmacro()

macro(createPlatform name)
    set(platformname "${name}-platform")
    add_custom_command(
        OUTPUT ${platformname}.tar.gz ${platformname}-rpmdb.tar.gz
        COMMAND ${CMAKE_COMMAND} -E cmake_echo_color --cyan "Building ${platformname}"
        COMMAND ${CMAKE_CURRENT_SOURCE_DIR}/setup_root.sh ${PLATFORM_BASE_IMAGE} > /dev/null
        COMMAND ${CMAKE_CURRENT_SOURCE_DIR}/build.sh rpm -Uvh `cat ${platformname}-packages`
        COMMAND tar --transform "s,^build/root/usr,files,S" -czf ${platformname}.tar.gz build/root/usr --owner=root > /dev/null
        COMMAND tar --transform "s,^build/var,files,S" -czf ${platformname}-rpmdb.tar.gz build/var/lib/rpm --owner=root > /dev/null
        COMMAND ${CMAKE_CURRENT_SOURCE_DIR}/clear_root.sh
        DEPENDS ${${platformname}_target} ${PLATFORM_BASE_IMAGE}
    )
endmacro()

macro(parseSPECFile package specFile sourcesList depsList)
    execute_process(COMMAND ${CMAKE_COMMAND} -E echo_append "-- Parsing SPEC file for package ${package}")
    # The path must be relative - we use it as both target name and actual file path,
    # but absolute paths differ here and in chroot in build.sh
    execute_process(COMMAND rpmspec -D "dist .sdk" -q ${specFile} --qf "%{NAME}=packages/RPMS/%{ARCH}/%{NAME}-%{VERSION}-%{RELEASE}.%{ARCH}.rpm;"
                    OUTPUT_VARIABLE rawProvidesList)
    execute_process(COMMAND rpmspec -D "dist .sdk" -q ${specFile} --buildrequires
                    OUTPUT_VARIABLE rawBuildRequiresList)
#    execute_process(COMMAND rpmspec -D "dist .sdk" -q ${specFile} --requires
#                    OUTPUT_VARIABLE rawRequiresList)
    execute_process(COMMAND rpmspec -D "dist .sdk" -P ${specFile}
                    OUTPUT_VARIABLE parsedFile)

    foreach(provides ${rawProvidesList})
        STRING(REGEX MATCH "^([0-9a-zA-Z_-]+)=(.*)$" match ${provides})
        set(${CMAKE_MATCH_1}_target ${CMAKE_MATCH_2})
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

    execute_process(COMMAND ${CMAKE_COMMAND} -E echo " -- done")
endmacro()

macro(generatePackageTargets platform packages)
    if (NOT EXISTS "${CMAKE_SOURCE_DIR}/packages/SOURCES")
        FILE(MAKE_DIRECTORY "${CMAKE_SOURCE_DIR}/packages/SOURCES")
    endif()

    foreach(package ${packages})
        set(specFile "${CMAKE_SOURCE_DIR}/packages/SPECS/${platform}-platform/${package}.spec")
        if (NOT EXISTS "${specFile}")
            message(FATAL_ERROR "SPEC file for package ${package} does not exist: ${specFile}")
        endif()

        parseSPECFile(${package} ${specFile} ${package}_sources ${package}_deps)
    endforeach()


    # Generate targets for each package:
    # ${package} (meta target)
    #  '-- ${package}-build (build)
    #       '-- ${package}-sources (get sources)
    foreach(package ${packages})
        add_custom_target(${package})

        # Use relative path to SPEC file, because absolute paths differ here and in the build.sh chroot
        set(specFile "packages/SPECS/${platform}-platform/${package}.spec")

        # List of local source tarballs
        set(sourceFiles "")
        foreach(source ${${package}_sources})
            get_filename_component(fileName ${source} NAME)
            set(destFile "${CMAKE_SOURCE_DIR}/packages/SOURCES/${fileName}")
            LIST(APPEND sourceFiles ${destFile})

            add_custom_command(
                OUTPUT ${destFile}
                COMMAND ${CMAKE_COMMAND} -E cmake_echo_color --cyan \"Downloading source for ${package}\"
                COMMAND if [ -e ${destFile} ]; then echo \"${destFile} already exists\"\; else wget ${source} -O ${destFile}\; fi
                DEPENDS ${specFile}
            )
        endforeach()
        if ("${sourceFiles}")
            # Only create the ${package}-source target if there are any sources
            add_custom_target(${package}-sources
                DEPENDS ${destFiles}
            )
            add_dependencies(${package} ${package}-sources)
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
        endforeach()

        add_custom_command(
            OUTPUT ${targets}
            COMMAND ${CMAKE_COMMAND} -E cmake_echo_color --cyan \"Building ${package}\"
            COMMAND ${CMAKE_COMMAND} -E cmake_echo_color --green \"* Preparing build root ...\"
            COMMAND ${CMAKE_SOURCE_DIR}/setup.sh ${SDK_BASE_IMAGE} > /dev/null
            COMMAND ${CMAKE_COMMAND} -E cmake_echo_color --green \"* Installing dependencies ...\"
            COMMAND ${installDeps}
            COMMAND ${CMAKE_COMMAND} -E cmake_echo_color --green \"* Building ...\"
            COMMAND ${CMAKE_SOURCE_DIR}/build.sh rpmbuild --clean -bb ${specFile} | tee packages/LOGS/${package}.build
            COMMAND ${CMAKE_COMMAND} -E cmake_echo_color --green \"* Cleaning up build root ...\"
            COMMAND ${CMAKE_SOURCE_DIR}/clear_root.sh
            COMMAND ${CMAKE_COMMAND} -E cmake_echo_color --green \"* Done\"
            DEPENDS ${SDK_BASE_IMAGE} ${PLATFORM_BASE_IMAGE} ${specFile} ${sourceFiles} ${depsPackages}
        )
        add_custom_target(${package}-build
            DEPENDS ${targets}
        )
        add_dependencies(${package} ${package}-build)

    endforeach()
endmacro()

macro(createBaseImages)
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

endmacro()


######### Build targets ##########

# Clone git.gnome.org/freedesktop-sdk-base with the yocto base
# it will generate the ${SDK_BASE_IMAGE} and ${PLATFORM_BASE_IMAGE} files
createBaseImages()

# Generates targets for all listed packages in freedesktop-platform
generatePackageTargets("freedesktop" "${freedesktop_PACKAGES}")


# freedesktop-sdk.tar.gz freedesktop-sdk-rpmdb.tar.gz
createSDK(freedesktop)
# kde-sdk.tar.gz, kde-sdk-rpmdb.tar.gz
#createSDK(kde)

# freedesktop-platform.tar.gz freedesktop-platform-rpmdb.tar.gz
createPlatform(freedesktop)
# kde-platform.tar.gz kde-platform-rpmdb.tar.gz
#createPlatform(kde)


#add_custom_target(kde-sdk-images ALL
#    DEPENDS kde-sdk.tar.gz kde-sdk-rpmdb.tar.gz
#)
add_custom_target(kde-sdk-images ALL
    DEPENDS freedesktop-sdk.tar.gz freedesktop-sdk-rpmdb.tar.gz
)

