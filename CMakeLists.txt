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

set(qt5_PACKAGES
    qt5-sdk-base

    qt5-platform
    qt5-sdk

    # pcre16 and pcre32 not provided by yocto
    pcre
    # qtbase, qtwayland
    #libudev

    # qtbase
    at-spi2-core
    alsa-lib
    xcb-util
    xcb-util-image
    xcb-util-keysyms
    xcb-util-renderutil
    xcb-util-wm
    #NetworkManager

    # glx detection
    mesa-libGLU
    glew
    mesa-demos

    # qttools
    clucene

    # qtimageformats
    libmng
    #libjasper

    # qtsensors
    #geoclue
    #gypsy

    # qtconnectivity
    #libical
    #bluez

    # qtmultimedia
    portaudio
    openal-soft
    #xv
    #gstreamer1-plugins-bad-free

    phonon
    phonon-backend-gstreamer

    # Bootstrap qttools
    qt5-qtbase-bootstrap
    qt5-qtxmlpatterns-bootstrap
    qt5-qtdeclarative-bootstrap
    qt5-qtlocation-bootstrap
    qt5-qtsensors-bootstrap
    qt5-qtwebkit-bootstrap
    qt5-qttools-bootstrap

    # Build normal qt5-qttools against bootstrap
    qt5-qttools

    # Build the rest of Qt5 with normal qttools
    qt5-qtbase
    qt5-qtdeclarative
    #qt5-qtconnectivity # missing bluez
    qt5-qtgraphicaleffects
    qt5-qtimageformats
    qt5-qtlocation
    qt5-qtmultimedia
    qt5-qtquick1
    qt5-qtquickcontrols
    qt5-qtscript
    qt5-qtsensors
    qt5-qtserialport
    qt5-qtsvg
    qt5-qttranslations
    #qt5-qtwayland # too old xkbcommon
    qt5-qtwebkit
    qt5-qtx11extras
    qt5-qtxmlpatterns
)

set(kf5_PACKAGES
    kf5-sdk-base
    kf5-sdk
    kf5-platform

    dbusmenu-qt5
    sgml-common
    docbook-dtds
    docbook-style-xsl
    fdupes
    giflib
    ilmbase
    libupnp
    OpenEXR
    boost

    extra-cmake-modules
    kf5

    kf5-attica
    kf5-frameworkintegration
    kf5-kactivities
    kf5-kapidox
    kf5-karchive
    kf5-kauth
    kf5-kbookmarks
    kf5-kcmutils
    kf5-kcodecs
    kf5-kcompletion
    kf5-kconfig
    kf5-kconfigwidgets
    kf5-kcoreaddons
    kf5-kcrash
    kf5-kdbusaddons
    kf5-kdeclarative
    kf5-kded
    kf5-kdelibs4support
    kf5-kdesignerplugin
    kf5-kdesu
    kf5-kdewebkit
    kf5-kdnssd
    kf5-kdoctools
    kf5-kemoticons
    kf5-kglobalaccel
    kf5-kguiaddons
    kf5-khtml
    kf5-ki18n
    kf5-kiconthemes
    kf5-kidletime
    kf5-kimageformats
    kf5-kinit
    kf5-kio
    kf5-kitemmodels
    kf5-kitemviews
    kf5-kjobwidgets
    kf5-kjsembed
    kf5-kjs
    kf5-kmediaplayer
    kf5-knewstuff
    kf5-knotifications
    kf5-knotifyconfig
    kf5-kpackage
    kf5-kparts
    kf5-kpeople
    kf5-kplotting
    kf5-kpty
    kf5-kross
    kf5-krunner
    kf5-kservice
    kf5-ktexteditor
    kf5-ktextwidgets
    kf5-kunitconversion
    kf5-kwallet
    kf5-kwidgetsaddons
    kf5-kwindowsystem
    kf5-kxmlgui
    kf5-kxmlrpcclient
    #kf5-modemmanager-qt
    #kf5-networkmanager-qt
    kf5-plasma
    kf5-solid
    kf5-sonnet
    kf5-threadweaver

    breeze
    oxygen-icon-theme
    kio-extras
)


######## Custom Macros #########
function(createSDK name)
    set(sdkname "${name}-sdk")
    add_custom_command(
        OUTPUT ${sdkname}.tar.gz ${sdkname}-rpmdb.tar.gz
        COMMAND ${CMAKE_CURRENT_SOURCE_DIR}/setup.sh ${SDK_BASE_IMAGE} > /dev/null
        COMMAND ${CMAKE_CURRENT_SOURCE_DIR}/build.sh smart install -y ${NOARCH}/${sdkname}-0.1-1.sdk.noarch.rpm
        COMMAND ${CMAKE_COMMAND} -E remove -f ${sdkname}.tar.gz ${sdkname}-rpmdb.tar.gz
        COMMAND tar --transform "s,^build/root/usr,files,S" -czf ${sdkname}.tar.gz build/root/usr --owner=root > /dev/null
        COMMAND tar --transform "s,^build/var,files,S" -czf ${sdkname}-rpmdb.tar.gz build/var/lib/rpm --owner=root > /dev/null
        COMMAND ${CMAKE_COMMAND} -E cmake_echo_color --green \"* Cleaning up build root ...\"
        COMMAND ${CMAKE_COMMAND} -E remove_directory ${CMAKE_CURRENT_SOURCE_DIR}/build/root
        COMMAND ${CMAKE_COMMAND} -E remove_directory ${CMAKE_CURRENT_SOURCE_DIR}/build/var
        COMMAND ${CMAKE_COMMAND} -E cmake_echo_color --green \"* Done\"
        DEPENDS ${${sdkname}_target} ${SDK_BASE_IMAGE}
        VERBATIM
    )
endfunction()

function(createPlatform name packages)
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
    set(platformname "${name}-platform")
    add_custom_command(
        OUTPUT ${platformname}.tar.gz ${platformname}-rpmdb.tar.gz
        COMMAND ${CMAKE_COMMAND} -E cmake_echo_color --cyan "Building ${platformname}"
        COMMAND ${CMAKE_CURRENT_SOURCE_DIR}/setup_root.sh ${PLATFORM_BASE_IMAGE} > /dev/null
        COMMAND ${CMAKE_CURRENT_SOURCE_DIR}/build.sh rpm -Uvh --nodeps ${installablePkgs}
        COMMAND tar --transform "s,^build/root/usr,files,S" -czf ${platformname}.tar.gz build/root/usr --owner=root > /dev/null
        COMMAND tar --transform "s,^build/var,files,S" -czf ${platformname}-rpmdb.tar.gz build/var/lib/rpm --owner=root > /dev/null
        COMMAND ${CMAKE_COMMAND} -E cmake_echo_color --green \"* Cleaning up build root ...\"
        COMMAND ${CMAKE_COMMAND} -E remove_directory ${CMAKE_CURRENT_SOURCE_DIR}/build/root
        COMMAND ${CMAKE_COMMAND} -E remove_directory ${CMAKE_CURRENT_SOURCE_DIR}/build/var
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
        set(specFile "${CMAKE_SOURCE_DIR}/packages/SPECS/${platform}-platform/${package}.spec")
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
        add_custom_target(${package})

        # Use relative path to SPEC file, because absolute paths differ here and in the build.sh chroot
        set(specFile "packages/SPECS/${platform}-platform/${package}.spec")

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
            LIST(APPEND ${allTargets} ${${tgt}_target})
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
            COMMAND ${CMAKE_COMMAND} -E remove_directory ${CMAKE_CURRENT_SOURCE_DIR}/build/root
            COMMAND ${CMAKE_COMMAND} -E remove_directory ${CMAKE_CURRENT_SOURCE_DIR}/build/var
            COMMAND ${CMAKE_COMMAND} -E cmake_echo_color --green \"* Done\"
            DEPENDS ${SDK_BASE_IMAGE} ${PLATFORM_BASE_IMAGE} ${specFile} ${sourceFiles} ${depsPackages}
        )
        add_custom_target(${package}-build
            DEPENDS ${targets}
        )
        add_dependencies(${package} ${package}-build)

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
        add_custom_command(OUTPUT ${uri}.repo
                           COMMAND if [ ! -d repo ]\; then ostree init --mode=archive-z2 --repo=repo else \"Using existing repo\"\; fi
                           COMMAND ${CMAKE_SOURCE_DIR}/commit.sh repo ${name}-${type}.tar.gz ${name}-${type}-rpmdb.tar.gz metadata.${name}.${type} ${uri} ${BUILD_ARCH} ${version}
                           COMMAND ${CMAKE_COMMAND} -E touch ${CMAKE_SOURCE_DIR}/${uri}.repo
                           DEPENDS ${name}-${type}.tar.gz ${name}-${type}-rpmdb.tar.gz
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

######### Build targets ##########

# Clone git.gnome.org/freedesktop-sdk-base with the yocto base
# it will generate the ${SDK_BASE_IMAGE} and ${PLATFORM_BASE_IMAGE} files
createBaseImages()

set(allPackages)

generatePackageTargets("freedesktop" "${freedesktop_PACKAGES}" allPackages)
createPlatform(freedesktop "${allPackages}")
createSDK(freedesktop)

generatePackageTargets("qt5" "${qt5_PACKAGES}" allPackages)
createPlatform(qt5 "${allPackages}")
createSDK(qt5)

generatePackageTargets("kf5" "${kf5_PACKAGES}" allPackages)
createPlatform(kf5 "${allPackages}")
createSDK(kf5)

add_custom_target(kde-sdk-images ALL
    DEPENDS freedesktop-sdk.tar.gz
            freedesktop-sdk-rpmdb.tar.gz
            qt5-sdk.tar.gz
            qt5-sdk-rpmdb.tar.gz
            kf5-sdk.tar.gz
            kf5-sdk-rpmdb.tar.gz
)

commit(Qt5 ${QT5_VERSION})
commit(KF5 ${KF5_VERSION})

#untag(Qt5 ${QT5_VERSION})
#untag(KF5 ${KF5_VERSION})

add_custom_target(repo ALL
    DEPENDS org.kde.Qt5.Platform.repo
            org.kde.Qt5.Sdk.repo
            org.kde.KF5.Platform.repo
            org.kde.KF5.Sdk.repo
)
