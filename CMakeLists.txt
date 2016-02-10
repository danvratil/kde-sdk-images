project(kde-sdk-images)
cmake_minimum_required(VERSION 3.0)

# Dan's magical build script


# These are versions of the final runtimes
# TODO: Make this somehow support multiple versions
set(FREEDESKTOP_VERSION "1.0")
set(QT5_VERSION "5.4.1")
set(KF5_VERSION "5.9.0")
set(BUILD_ARCH "x86_64")
# Revision of the used Yocto base
set(BASE_HASH "8e44c998adbf1546c45cf733c688fed74e8ddc89")
set(NOARCH "packages/RPMS/noarch")

# This is where the ostree repository will be created
set(REPO_PATH "repo")

# This is where the built Yocto image will be created
# The Yocto image is basically a tarball with base filesystem
set(IMAGE_DIR "${CMAKE_SOURCE_DIR}/freedesktop-sdk-base/images/${BUILD_ARCH}")

# These are names of the freedesktop images, which are just tarballs with filesystems
# Images include the freedesktop yocto base (freedesktop-sdk-base) + all the packages
# listed below in freedesktop_PACKAGES
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

# createSDK(name)
#
# Creates SDK images (tarballs) for given ${name}
#
function(createSDK name)
    set(sdkname "${name}-sdk")
    add_custom_command(
        OUTPUT ${sdkname}.tar.gz ${sdkname}-rpmdb.tar.gz
    	# Extracts Yocto base image to build/root
        COMMAND ${CMAKE_CURRENT_SOURCE_DIR}/setup.sh ${SDK_BASE_IMAGE}
	    # Installs an SDK metapackage into the build/root basedir, this makes
	    # sure that all SDK packages are installed (via RPM dependencies) into
	    # the runtime.
	    # TODO: The version of the metapackage is hardcoded here, so it needs to
	    # be bumped manually when you bump the metapackage version (which happens)
        COMMAND ${CMAKE_CURRENT_SOURCE_DIR}/build.sh smart install -y ${NOARCH}/${sdkname}-0.1-2.sdk.noarch.rpm
	    # Removes old SDK images
        COMMAND ${CMAKE_COMMAND} -E remove -f ${sdkname}.tar.gz ${sdkname}-rpmdb.tar.gz
	    # Creates new SDK images (tar.gz archives) by tarring content of build/root/usr and build/var/lib/rpm.
	    # It rewrites build/root/usr and build/var to /files, which is the root folder in runtimes
        COMMAND tar --transform "s,^build/root/usr,files,S" -czf ${sdkname}.tar.gz build/root/usr --owner=root
        COMMAND tar --transform "s,^build/var,files,S" -czf ${sdkname}-rpmdb.tar.gz build/var/lib/rpm --owner=root
        COMMAND ${CMAKE_COMMAND} -E cmake_echo_color --green \"* Cleaning up build root ...\"
        COMMAND ${CMAKE_COMMAND} -E remove_directory ${CMAKE_CURRENT_SOURCE_DIR}/build/root
        COMMAND ${CMAKE_COMMAND} -E remove_directory ${CMAKE_CURRENT_SOURCE_DIR}/build/var
        COMMAND ${CMAKE_COMMAND} -E cmake_echo_color --green \"* Done\"
        DEPENDS ${${sdkname}_target} ${SDK_BASE_IMAGE}
        VERBATIM
    )
endfunction()

#
# createPlatform(name, packages)
#
# Creates platform images (tarballs) for given platform ${name} containing
# ${packages}.
#
# ${packages} contains *all* RPMs provided by all SPECfiles for the given
# runtime, i.e. foo-1.0-1.x86.64.rpm, foo-dev-1.0-1.x64_64.rpm, foo-debuginfo-1.0-1.x86_64.rpm
# etc.
function(createPlatform name packages)
    # Packages that we actually want to install, i.e. excluding -dev, -debuginfo and
    # and other packages that belong to SDK but not Platform
    set(installablePkgs)
    foreach (package ${packages})
        set(exclude "FALSE")
	    # Packages to skip: -dev, -debuginfo, -sdk, -static, -bootstrap (see Qt packages)
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
    	# Extract the Yocto base image to build/root
        COMMAND ${CMAKE_CURRENT_SOURCE_DIR}/setup_root.sh ${PLATFORM_BASE_IMAGE} > /dev/null
	    # Install all the RPMs to build/root
        COMMAND ${CMAKE_CURRENT_SOURCE_DIR}/build.sh rpm -Uvh --nodeps ${installablePkgs}
	    # Tar it up like in SDK
        COMMAND tar --transform "s,^build/root/usr,files,S" -czf ${platformname}.tar.gz build/root/usr --owner=root > /dev/null
        COMMAND tar --transform "s,^build/var,files,S" -czf ${platformname}-rpmdb.tar.gz build/var/lib/rpm --owner=root > /dev/null
        COMMAND ${CMAKE_COMMAND} -E cmake_echo_color --green \"* Cleaning up build root ...\"
        COMMAND ${CMAKE_COMMAND} -E remove_directory ${CMAKE_CURRENT_SOURCE_DIR}/build/root
        COMMAND ${CMAKE_COMMAND} -E remove_directory ${CMAKE_CURRENT_SOURCE_DIR}/build/var
        COMMAND ${CMAKE_COMMAND} -E cmake_echo_color --green \"* Done\"
        DEPENDS ${${platformname}_target} ${PLATFORM_BASE_IMAGE}
    )
endfunction()

#
# parseSPECFile(package, specFile, sourcesList, depsList)
#
# package: name of the package (foo)
# specFile: relative path to the specfile (packages/SPECS/bar/foo.spec). The path must be relative,
#           because we use it both as target name and actual file path. But absolute paths differ
#           here and in chroot in build.sh. The paths are relative to current working directory.
# sourcesList (out): will be populated with list of Sources (URLs) from the SPEC file
# depsList (out): will be populated with list of package names that are dependencies of this ${package}

function(parseSPECFile package specFile sourcesList depsList)
    execute_process(COMMAND ${CMAKE_COMMAND} -E echo_append "-- Parsing SPEC file for package ${package}")
    # Gets full list of packages names that this SPEC file provides in format described in --qf switch
    execute_process(COMMAND rpmspec -D "_topdir ${CMAKE_SOURCE_DIR}/packages" -D "dist .sdk" -q ${specFile} --qf "%{NAME}=packages/RPMS/%{ARCH}/%{NAME}-%{VERSION}-%{RELEASE}.%{ARCH}.rpm;"
                    OUTPUT_VARIABLE rawProvidesList)
    # Gets full list of BuildRequires
    execute_process(COMMAND rpmspec -D "_topdir ${CMAKE_SOURCE_DIR}/packages" -D "dist .sdk" -q ${specFile} --buildrequires
                    OUTPUT_VARIABLE rawBuildRequiresList)
    # Gets full list of Requires
#    execute_process(COMMAND rpmspec -D "_topdir ${CMAKE_SOURCE_DIR}/packages" -D "dist .sdk" -q ${specFile} --requires
#                    OUTPUT_VARIABLE rawRequiresList)
    # Parses the whole SPEC file and outputs it to parsedFile variable. This includes expanding
    # all variables in the SPEC file, evaluating all conditions etc.
    execute_process(COMMAND rpmspec -D "_topdir ${CMAKE_SOURCE_DIR}/packages" -D "dist .sdk" -P ${specFile}
                    OUTPUT_VARIABLE parsedFile)

    # The content of rawProvidesList is something like
    #   foo=packages/RPMS/x86_64/foo-1.0-1.x86_64.rpm
    #   foo-devel=packages/RPMS/x86_64/foo-devel-1.0-1.x86_64.rpm
    #   etc.
    # It is parsed here an turned it into variables, i.e. it expands to
    #   (variable) = (value)
    #   foo_target = packages/RPMS/x86_64/foo-1.0-1.x86_64.rpm
    #   foo-devel_target = packages/RPMS/x86_64/foo-1.0-1.x86_64.rpm
    #   etc.
    #
    # Finally it adds list of all the package names (foo, foo-devel, ...) into
    # ${package}_targets, e.g.  foo_targets.
    #
    foreach(provides ${rawProvidesList})
        STRING(REGEX MATCH "^([0-9a-zA-Z_-]+)=(.*)$" match ${provides})
        set(${CMAKE_MATCH_1}_target ${CMAKE_MATCH_2})
        set(${CMAKE_MATCH_1}_target ${CMAKE_MATCH_2} PARENT_SCOPE)
        LIST(APPEND ${package}_targets ${CMAKE_MATCH_1})
    endforeach()

    # Black magic: this turns new-line-separeted list of rawBuildRequiresList
    # into a CMake semicolon-separated list. The first regexp escapes existing
    # semicolons, the second one replaces newlines with CMake list separators (semicolons)
    STRING(REGEX REPLACE ";" "\\\\;" rawBuildRequiresList "${rawBuildRequiresList}")
    STRING(REGEX REPLACE "\n" ";" buildRequiresList "${rawBuildRequiresList}")
    # Appends the list of dependencies to the depsList variable passed to this method.
    LIST(APPEND ${depsList} ${buildRequiresList})

#    STRING(REGEX REPLACE ";" "\\\\;" rawRequiresList "${rawRequiresList}")
#    STRING(REGEX REPLACE "\n" ";" requiresList "${rawRequiresList}")
#    LIST(APPEND ${depsList} ${requiresList})

    # Convert parsedFile to a CMake list by converting new lines to semicolons,
    # so that we can iterate over the file line-by-line
    STRING(REGEX REPLACE ";" "\\\\;" parsedFile "${parsedFile}")
    STRING(REGEX REPLACE "\n" ";" parsedFile "${parsedFile}")
    foreach(line ${parsedFile})
        # Look for all Sources
        STRING(REGEX MATCHALL "^Source[0-9]*:(.*)$" matches "${line}")
        if (NOT "${CMAKE_MATCH_1}" STREQUAL "")
            STRING(STRIP "${CMAKE_MATCH_1}" urlStripped)
            # We are only interested in remote sources, so match by protocol
            if (${urlStripped} MATCHES "^(http|https|ftp):.*$")
                # If it's a remote source, add it to the sourcesList list
                LIST(APPEND ${sourcesList} "${urlStripped}")
            endif()
        endif()
    endforeach()

    # Export the variables to the parent scope, so that they are available
    # in caller's scope as well
    set(${package}_targets ${${package}_targets} PARENT_SCOPE)
    set(sourcesList ${sourcesList} PARENT_SCOPE)
    set(${depsList} ${${depsList}} PARENT_SCOPE)

    execute_process(COMMAND ${CMAKE_COMMAND} -E echo " -- done")
endfunction()

#
# generatePackageTargets(platform, packages, allTargets)
#
# Creates CMake targets for each package
#
function(generatePackageTargets platform packages allTargets)
    if (NOT EXISTS "${CMAKE_SOURCE_DIR}/packages/SOURCES")
        FILE(MAKE_DIRECTORY "${CMAKE_SOURCE_DIR}/packages/SOURCES")
    endif()

    # For each given package make sure the SPEC file exists, then parse it
    foreach(package ${packages})
        set(specFile "${CMAKE_SOURCE_DIR}/packages/SPECS/${platform}-platform/${package}.spec")
        if (NOT EXISTS "${specFile}")
            message(FATAL_ERROR "SPEC file for package ${package} does not exist: ${specFile}")
        endif()

        # Parse the SPEC file
        parseSPECFile(${package} ${specFile} ${package}_sources ${package}_deps)

        # Export the following variables to parent scope, so that they are available in
        # caller's scope as well. These were originally defined in parseSPECFile() and
        # exported to our scope.
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

    # allDestFiles is a list of all source files needed by all packages.
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
    	    # Make sure that the source file does not exist yet (i.e. it's not in allDestFiles)
            # This is necessary otherwise if two or more packages have the same tarball (happens!),
	        # CMake would abort on the add_custom_command() below, because we would be trying to create
      	    # an existing target multiple times.
            LIST(FIND allDestFiles ${destFile} found)
            if (${found} EQUAL -1)
  		        # If we haven't seen this source file before then add it to the list of allDestFiles and create
		        # a wget command to download it.
                LIST(APPEND allDestFiles ${destFile})
                add_custom_command(
                    OUTPUT ${destFile}
                    COMMAND ${CMAKE_COMMAND} -E cmake_echo_color --cyan \"Downloading source for ${package}\"
                    COMMAND if [ -e ${destFile} ]; then echo \"${destFile} already exists\"\; else wget ${source} -O ${destFile}\; fi
                    DEPENDS ${specFile}
                )
            endif()
        endforeach()
	    # Create ${package}-sources target only if there are any sources, otherwise CMake
	    # will complain that the DEPENDS list is empty.
        if ("${sourceFiles}")
            add_custom_target(${package}-sources
                DEPENDS ${destFiles}
            )
            add_dependencies(${package} ${package}-sources)
        endif()

	    # Go through all dependencies of each package (${$package}_deps}) and resolve
	    # them to filepaths to actual RPMs (that are in foo_target variables).
        set(depsPackages "")
        foreach(dep ${${package}_deps})
            LIST(APPEND depsPackages ${${dep}_target})
        endforeach()
	    # If the package has any dependencies, then remove potential duplicates, and
	    # store a command to install the dependencies into the buildroot in "installDeps"
	    # variable.
        if (depsPackages)
            # smart does not like duplicates
            LIST(REMOVE_DUPLICATES depsPackages)
            set(installDeps ${CMAKE_SOURCE_DIR}/build.sh smart install -y ${depsPackages})
        else()
	        # If there are no dependencies, then we will just invoke "true" command, which returns
	        # success, so that CMake is happy when invoking multiple commands in add_custom_command().
            set(installDeps true)
            set(depTargets "")
        endif()

	    # Store all targets (that is package names) in targets and allTargets variables.
        set(targets "")
        foreach(tgt ${${package}_targets})
            LIST(APPEND targets ${${tgt}_target})
            LIST(APPEND ${allTargets} ${${tgt}_target})
        endforeach()

        add_custom_command(
            OUTPUT ${targets}
            COMMAND ${CMAKE_COMMAND} -E cmake_echo_color --cyan \"Building ${package}\"
            COMMAND ${CMAKE_COMMAND} -E cmake_echo_color --green \"* Preparing build root ...\"
	        # Prepare the base SDK image by extracting it to build/root
            COMMAND ${CMAKE_SOURCE_DIR}/setup.sh ${SDK_BASE_IMAGE}
            COMMAND ${CMAKE_COMMAND} -E cmake_echo_color --green \"* Installing dependencies ...\"
	        # If there are any deps, install them into the build root.
            COMMAND ${installDeps}
            COMMAND ${CMAKE_COMMAND} -E cmake_echo_color --green \"* Building ...\"
	        # Now build the RPM for the current package, the build log is printed to screen as well as to
	        # a file.
            COMMAND ${CMAKE_SOURCE_DIR}/build.sh rpmbuild --clean -bb ${specFile} | tee packages/LOGS/${package}.build
            COMMAND ${CMAKE_COMMAND} -E cmake_echo_color --green \"* Cleaning up build root ...\"
            COMMAND ${CMAKE_COMMAND} -E remove_directory ${CMAKE_CURRENT_SOURCE_DIR}/build/root
            COMMAND ${CMAKE_COMMAND} -E remove_directory ${CMAKE_CURRENT_SOURCE_DIR}/build/var
            COMMAND ${CMAKE_COMMAND} -E cmake_echo_color --green \"* Done\"
            DEPENDS ${SDK_BASE_IMAGE} ${PLATFORM_BASE_IMAGE} ${specFile} ${sourceFiles} ${depsPackages}
        )
	    # Create a ${package}-build target that depends on all targets
	    # that represent dependencies of this package. That means that running
	    # "make foo" will make sure that all dependencies are built and available.
        add_custom_target(${package}-build
            DEPENDS ${targets}
        )
        add_dependencies(${package} ${package}-build)

    endforeach() # Go to next package.
    unset(allDestFiles)

    # Export the allTargets variable to parent scope
    set(${allTargets} ${${allTargets}} PARENT_SCOPE)
endfunction()

#
# createBaseImages()
#
# Clones and builds the Yocto base image. This takes something between
# forever and eternity.
#
# We don't maintain the Yocto clone in this repo, instead we the one from Gnome's
# freedesktop-sdk-base, which makes it easier for us and saves us ton of work.
#
function(createBaseImages)
    add_custom_command(OUTPUT ${CMAKE_SOURCE_DIR}/freedesktop-sdk-base/Makefile
                       COMMAND ${CMAKE_COMMAND} -E cmake_echo_color --cyan "Cloning freedesktop-sdk-base"
                       COMMAND git clone git://git.gnome.org/freedesktop-sdk-base
                       COMMAND cd freedesktop-sdk-base && git fetch origin
                       COMMAND cd freedesktop-sdk-base && git checkout ${BASE_HASH}
                       WORKING_DIRECTORY ${CMAKE_SOURCE_DIR}
    )

    # FIXME: Hardcoded -j5, could use more when using icecream or something.
    # This will generate the base images (tarballs)
    add_custom_command(OUTPUT ${SDK_BASE_IMAGE} ${PLATFORM_BASE_IMAGE}
                       COMMAND make -j5
                       WORKING_DIRECTORY ${CMAKE_SOURCE_DIR}/freedesktop-sdk-base
                       DEPENDS "${CMAKE_SOURCE_DIR}/freedesktop-sdk-base/Makefile"
    )

endfunction()

#
# commit(name, version)
#
# Commits Platform and SDK for given runtime of given version.
#
function(commit name version)
    # Helper function that does the actual commit
    function(_commit type uri name version)
	    # HACK: This will create an org.kde.foo.repo file after the commit. If you want
	    # to make a new commit, you need to remove the file first, otherwise CMake will
	    # think there's "nothing to do", since the file already exists.
	    # This is a workaround for CMake requiring add_custom_command() to always generate
	    # some file.
        add_custom_command(OUTPUT ${uri}.repo
		    	           # If the ostree repo does not exist it will be created
                           COMMAND if [ ! -d ${REPO_PATH}  ]\; then ostree init --mode=archive-z2 --repo=${REPO_PATH} else \"Using existing repo\"\; fi
			               # Does the actual commit - this takes forever.
                           COMMAND ${CMAKE_SOURCE_DIR}/commit.sh repo ${name}-${type}.tar.gz ${name}-${type}-rpmdb.tar.gz metadata.${name}.${type} ${uri} ${BUILD_ARCH} ${version}
                           COMMAND ${CMAKE_COMMAND} -E touch ${CMAKE_SOURCE_DIR}/${uri}.repo
                           DEPENDS ${name}-${type}.tar.gz ${name}-${type}-rpmdb.tar.gz
        )
    endfunction()

    STRING(TOLOWER ${name} lcname)
    _commit(platform org.kde.${name}.Platform ${lcname} ${version})
    _commit(sdk org.kde.${name}.Sdk ${lcname} ${version})
endfunction()

#
# untag(name, version)
#
# I'll be honest with you: I have no idea what this does.
#
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

# Clone git.gnome.org/freedesktop-sdk-base with the yocto base.
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

# Creates a "kde-sdk-images" target, which generates all images
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

# Creates a "repo" target, which commits all images to OSTREE repository
add_custom_target(repo ALL
    DEPENDS org.kde.Qt5.Platform.repo
            org.kde.Qt5.Sdk.repo
            org.kde.KF5.Platform.repo
            org.kde.KF5.Sdk.repo
)
