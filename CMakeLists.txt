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

include("${CMAKE_SOURCE_DIR}/functions.cmake")

set(freedesktop-1.0_PACKAGES
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

set(qt5-5.4.1_PACKAGES
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

set(kf5-5.9.0_PACKAGES
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

set(kf5-5.12.0_PACKAGES ${kf5-5.9.0_PACKAGES})



function buildRuntime(uri name version dependencies)
    set(allPackages)
    foreach(dependency "${dependencies}")
        generatePackageTargets(${dependency} ${${dependency}_PACKAGES} allPackages)
        createPlatform(${dependency) ${${dependency}_PACKAGES})
        createSDK(${dependency})
    endforeach()

    createPlatform(${name}-${version} ${${name}-${version}_PACKAGES})
    createSDK(${name}-${version})

    commit(${uri} ${version})
endfunction()

######### Build targets ##########

# Clone git.gnome.org/freedesktop-sdk-base with the yocto base
# it will generate the ${SDK_BASE_IMAGE} and ${PLATFORM_BASE_IMAGE} files
createBaseImages()

set(fdPackages)
generatePackageTargets(freedesktop-1.0 "${freedesktop_PACKAGES}" fdPackages)

set(qtPackages ${fdPackages})
generatePackageTargets(qt5-5.4.1 "${qt5_PACKAGES}" qtPackages)

set(kf5_5-9-0_packages ${qtPackages})
generatePackageTargets(kf5-5.9.0 "${kf5_PACKAGES}" kf5_5-9-0_packages)

set(kf5_5-12-0_packages ${qtPackages})
generatePackageTargets(kf5-5.12.0 "${kf5_PACKAGES}" kf5_5-12-0_packages)
message(STATUS "${kf5_5-12-0_packages}")

createPlatform(freedesktop 1.0 "${fdPackages}")
createSDK("freedesktop" "1.0" "1")

createPlatform("qt5" "5.4.1" "${qtPackages}")
createSDK("qt5" "5.4.1" "1")

createPlatform("kf5" "5.9.0" "${kf5_5-9-0_packages}")
createSDK("kf5" "5.9.0" "1")

createPlatform("kf5" "5.12.0" "${kf5_5-12-0_packages}")
createSDK("kf5" "5.12.0" "1")

add_custom_target(kde-sdk-images ALL
    DEPENDS freedesktop-sdk-1.0.tar.gz
            freedesktop-sdk-1.0-rpmdb.tar.gz
            qt5-sdk-5.4.1.tar.gz
            qt5-sdk-5.4.1-rpmdb.tar.gz
            kf5-sdk-5.9.0.tar.gz
            kf5-sdk-5.9.0-rpmdb.tar.gz
            kf5-sdk-5.12.0.tar.gz
            kf5-sdk-5.12.0-rpmdb.tar.gz
)

commit("org.kde.Qt5" "5.4.1")
commit("org.kde.KF5" "5.9.0")
commit("org.kde.KF5" "5.12.0")

#untag(Qt5 ${QT5_VERSION})
#untag(KF5 ${KF5_VERSION})

add_custom_target(repo ALL
    DEPENDS org.kde.Qt5.Platform-5.4.1.repo
            org.kde.Qt5.Sdk-5.4.1.repo
            org.kde.KF5.Platform-5.9.0.repo
            org.kde.KF5.Sdk-5.9.0.repo
            org.kde.KF5.Platform-5.12.0.repo
            org.kde.KF5.Sdk-5.12.0.repo
)
