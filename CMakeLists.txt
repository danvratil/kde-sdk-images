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
    cairo
    dbus-glib
    dbus
    dejavu-fonts
    desktop-file-utils
    fontconfig
    freetype
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
    libdrm
    libepoxy
    liberation-fonts
    libICE
    libpciaccess
    libproxy
    libSM
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
        DEPENDS ${sdkname} ${SDK_BASE_IMAGE}
        COMMAND ${CMAKE_CURRENT_SOURCE_DIR}/setup.sh ${SDK_BASE_IMAGE}
        COMMAND ${CMAKE_CURRENT_SOURCE_DIR}/build.sh smart install -y ${NOARCH}/${sdkname}-0.1-1.sdk.noarch.rpm
        COMMAND rm -rf ${sdkname}.tar.gz ${sdkname}-rpmdb.tar.gz
        COMMAND tar --transform 's,^build/root/usr,files,S' -czf ${sdkname}.tar.gz build/root/usr --owner=root
        COMMAND tar --transform 's,^build/var,files,S' -czf ${sdkname}-rpmdb.tar.gz build/var/lib/rpm --owner-root
        COMMAND ${CMAKE_CURRENT_SOURCE_DIR}/clear_root.sh
        VERBATIM
    )
endmacro()

macro(createPlatform name)
    set(platformname "${name}-platform")
    add_custom_command(
        OUTPUT ${platformname}.tar.gz ${platformname}-rpmdb.tar.gz
        COMMAND ${CMAKE_COMMAND} -E cmake_echo_color --cyan "Building ${platformname}"
        COMMAND ${CMAKE_CURRENT_SOURCE_DIR}/setup_root.sh ${PLATFORM_BASE_IMAGE}
        COMMAND ${CMAKE_CURRENT_SOURCE_DIR}/build.sh rpm -Uvh `cat ${platformname}-packages`
        COMMAND tar --transform 's,^build/root/usr,files,S' -czf ${platformname}.tar.gz build/root/usr --owner=root
        COMMAND tar --transform 's,^build/var,files,S' -czf ${platformname}-rpmdb.tar.gz build/var/lib/rpm --owner=root
        COMMAND ${CMAKE_CURRENT_SOURCE_DIR}/clear_root.sh
        DEPENDS ${platformname} ${PLATFORM_BASE_IMAGE}
    )
endmacro()

macro(createFreedesktopPlatformBase)
    add_custom_command(
        OUTPUT freedesktop-platform-base-0.1-1.sdk.noarch.rpm
        COMMAND ${CMAKE_COMMAND} -E cmake_echo_color --cyan "Building freedesktop-platform-base"
        COMMAND rm -rf packages/freedesktop-platform
        COMMAND mkdir -p packages/freedesktop-platform
        COMMAND tar -C packages/freedesktop-platform -xzf ${PLATFORM_BASE_IMAGE}
        COMMAND ${CMAKE_CURRENT_SOURCE_DIR}/setup.sh ${SDK_BASE_IMAGE}
        COMMAND ${CMAKE_CURRENT_SOURCE_DIR}/build.sh rpmbuild -ba ${CMAKE_CURRENT_SOURCE_DIR}/packages/SPECS/freedesktop-platform/freedesktop-platform-base.spec
        COMMAND ${CMAKE_CURRENT_SOURCE_DIR}/clear_root.sh
        DEPENDS ${SDK_BASE_IMAGE} ${PLATFORM_BASE_IMAGE}
    )
endmacro()

macro(parseSPECFile package specFile sourcesList buildRequiresList)
    # The path must be relative - we use it as both target name and actual file path,
    # but absolute paths differ here and in chroot in build.sh
    execute_process(COMMAND rpmspec -D "dist .sdk" -q ${specFile} --qf "%{NAME}=packages/RPMS/%{ARCH}/%{NAME}-%{VERSION}-%{RELEASE}.%{ARCH}.rpm;"
                    OUTPUT_VARIABLE rawProvidesList)
    execute_process(COMMAND rpmspec -D "dist .sdk" -q ${specFile} --buildrequires
                    OUTPUT_VARIABLE rawBuildRequiresList)
    execute_process(COMMAND rpmspec -D "dist .sdk" -P ${specFile}
                    OUTPUT_VARIABLE parsedFile)

    foreach(provides ${rawProvidesList})
        STRING(REGEX MATCH "^([0-9a-zA-Z_-]+)=(.*)$" match ${provides})
        set(${CMAKE_MATCH_1}_target ${CMAKE_MATCH_2})
        LIST(APPEND ${package}_targets ${CMAKE_MATCH_1})
    endforeach()

    STRING(REGEX REPLACE ";" "\\\\;" rawBuildRequiresList "${rawBuildRequiresList}")
    STRING(REGEX REPLACE "\n" ";" ${buildRequiresList} "${rawBuildRequiresList}")


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

        parseSPECFile(${package} ${specFile} ${package}_sources ${package}_buildRequires)
        message(STATUS "Parsing SPEC file for package ${package} -- done")
    endforeach()


    foreach(package ${packages})
        message(STATUS "Preparing package ${package}")
        # Use relative path to SPEC file, because absolute paths differ here and in the build.sh chroot
        set(specFile "packages/SPECS/${platform}-platform/${package}.spec")

        if (${package}_sources)
            foreach(source ${${package}_sources})
                get_filename_component(fileName ${source} NAME)
                set(destFile "${CMAKE_SOURCE_DIR}/packages/SOURCES/${fileName}")
                if (NOT EXISTS "${destFile}")
                    message(STATUS "\t* Downloading ${source}  ...")
                    # TODO: Check hashes
                    FILE(DOWNLOAD "${source}" "${destFile}"
                         STATUS status
                    )
                    LIST(GET ${status} 0 statusCode)
                    LIST(GET ${status} 1 statusMsg)
                    if (${statusCode} GREATER 0)
                        message(FATAL_ERROR "Failed to download source file for ${package}: ${statusMsg}")
                    endif()
                else()
                    message(STATUS "\t* Source file ${fileName} already exists, not re-downloading")
                endif()
            endforeach()
        else()
            message(STATUS "\t* No remote sources to download")
        endif()

        if (${package}_buildRequires)
            set(buildRequiresPackages "")
            foreach(br ${${package}_buildRequires})
                foreach (pkg ${${br}_provides})
                    set(buildRequiresPackages "${buildRequiresPackages} $pkg")
                endforeach()
            endforeach()
            set(installBuildRequires "${CMAKE_SOURCE_DIR}/build.sh smart install -y ${buildRequiresPackages}")
        else()
            set(installBuildRequires "${CMAKE_COMMAND} -E echo")
            set(buildRequiresPackages "")
        endif()

        message(STATUS "\t* Adding custom target ${${package}_provides}")

        add_custom_command(
            OUTPUT ${${package}_provides}
            COMMAND ${CMAKE_COMMAND} -E cmake_echo_color --cyan "Building ${package}"
            COMMAND ${CMAKE_COMMAND} -E cmake_echo_color --green "\t* Preparing build root ..."
            COMMAND ${CMAKE_SOURCE_DIR}/setup.sh ${SDK_BASE_IMAGE}
            COMMAND ${CMAKE_COMMAND} -E cmake_echo_color --green "\t* Installing dependencies ..."
            COMMAND ${installBuildRequires}
            COMMAND ${CMAKE_COMMAND} -E cmake_echo_color --green "\t* Building ..."
            COMMAND ${CMAKE_SOURCE_DIR}/build.sh rpmbuild --clean -bb ${specFile}
            COMMAND ${CMAKE_COMMAND} -E cmake_echo_color --green "\t* Cleaning up build root ..."
            COMMAND ${CMAKE_SOURCE_DIR}/clear_root.sh
            COMMAND ${CMAKE_COMMAND} -E cmake_echo_color --green "\t* Done"
            DEPENDS ${SDK_BASE_IMAGE} ${PLATFORM_BASE_IMAGE} ${buildRequiresPackages}
        )
        add_custom_target(${package}
            DEPENDS ${${package}_provides}
        )
    endforeach()
endmacro()

macro(createBaseImages)
    add_custom_command(OUTPUT ${CMAKE_SOURCE_DIR}/freedesktop-sdk-base
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
                       DEPENDS ${CMAKE_CURRENT_SOURCE_DIR}/freedesktop-sdk-base
    )

endmacro()


######### Build targets ##########

createBaseImages()

generatePackageTargets("freedesktop" "${freedesktop_PACKAGES}")


# freedesktop-sdk.tar.gz freedesktop-sdk-rpmdb.tar.gz
createSDK(freedesktop)
# kde-sdk.tar.gz, kde-sdk-rpmdb.tar.gz
#createSDK(kde)

# freedesktop-platform-bae-0.1-1.sdk.noarch.rpm
createFreedesktopPlatformBase()

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
