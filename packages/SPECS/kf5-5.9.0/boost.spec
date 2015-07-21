# Support for documentation installation As the %%doc macro erases the
# target directory ($RPM_BUILD_ROOT%%{_docdir}/%%{name}), manually
# installed documentation must be saved into a temporary dedicated
# directory.
# XXX note that as of rpm 4.9.1, this shouldn't be necessary anymore.
# We should be able to install directly.
%define boost_docdir __tmp_docdir
%define boost_examplesdir __tmp_examplesdir

Name: boost
Summary: The free peer-reviewed portable C++ source libraries
Version: 1.57.0
%define version_enc 1_57_0
Release: 1%{?dist}
License: Boost and MIT and Python

%define toplev_dirname %{name}_%{version_enc}
URL: http://www.boost.org
Group: System Environment/Libraries

Source0: http://downloads.sourceforge.net/%{name}/%{toplev_dirname}.tar.bz2
Source1: ver.py
Source2: libboost_thread.so

# Since Fedora 13, the Boost libraries are delivered with sonames
# equal to the Boost version (e.g., 1.41.0).
%define sonamever %{version}

# boost is an "umbrella" package that pulls in all other boost
# components, except for MPI and Python 3 sub-packages.  Those are
# special in that they are rarely necessary, and it's not a big burden
# to have interested parties install them explicitly.
Requires: boost-atomic%{?_isa} = %{version}-%{release}
Requires: boost-chrono%{?_isa} = %{version}-%{release}
Requires: boost-context%{?_isa} = %{version}-%{release}
Requires: boost-coroutine%{?_isa} = %{version}-%{release}
Requires: boost-date-time%{?_isa} = %{version}-%{release}
Requires: boost-filesystem%{?_isa} = %{version}-%{release}
Requires: boost-graph%{?_isa} = %{version}-%{release}
Requires: boost-iostreams%{?_isa} = %{version}-%{release}
Requires: boost-locale%{?_isa} = %{version}-%{release}
Requires: boost-log%{?_isa} = %{version}-%{release}
Requires: boost-math%{?_isa} = %{version}-%{release}
Requires: boost-program-options%{?_isa} = %{version}-%{release}
Requires: boost-python%{?_isa} = %{version}-%{release}
Requires: boost-random%{?_isa} = %{version}-%{release}
Requires: boost-regex%{?_isa} = %{version}-%{release}
Requires: boost-serialization%{?_isa} = %{version}-%{release}
Requires: boost-signals%{?_isa} = %{version}-%{release}
Requires: boost-system%{?_isa} = %{version}-%{release}
Requires: boost-test%{?_isa} = %{version}-%{release}
Requires: boost-thread%{?_isa} = %{version}-%{release}
Requires: boost-timer%{?_isa} = %{version}-%{release}
Requires: boost-wave%{?_isa} = %{version}-%{release}

BuildRequires: freedesktop-sdk-base

%bcond_with tests
%bcond_with docs_generated

%description
Boost provides free peer-reviewed portable C++ source libraries.  The
emphasis is on libraries which work well with the C++ Standard
Library, in the hopes of establishing "existing practice" for
extensions and providing reference implementations so that the Boost
libraries are suitable for eventual standardization. (Some of the
libraries have already been included in the C++ 2011 standard and
others have been proposed to the C++ Standards Committee for inclusion
in future standards.)

%package atomic
Summary: Run-Time component of boost atomic library
Group: System Environment/Libraries

%description atomic

Run-Time support for Boost.Atomic, a library that provides atomic data
types and operations on these data types, as well as memory ordering
constraints required for coordinating multiple threads through atomic
variables.

%package chrono
Summary: Run-Time component of boost chrono library
Group: System Environment/Libraries
Requires: boost-system%{?_isa} = %{version}-%{release}

%description chrono

Run-Time support for Boost.Chrono, a set of useful time utilities.

%package container
Summary: Run-Time component of boost container library
Group: System Environment/Libraries

%description container

Boost.Container library implements several well-known containers,
including STL containers. The aim of the library is to offers advanced
features not present in standard containers or to offer the latest
standard draft features for compilers that comply with C++03.

%package context
Summary: Run-Time component of boost context switching library
Group: System Environment/Libraries

%description context

Run-Time support for Boost.Context, a foundational library that
provides a sort of cooperative multitasking on a single thread.

%package coroutine
Summary: Run-Time component of boost coroutine library
Group: System Environment/Libraries

%description coroutine
Run-Time support for Boost.Coroutine, a library that provides
generalized subroutines which allow multiple entry points for
suspending and resuming execution.

%package date-time
Summary: Run-Time component of boost date-time library
Group: System Environment/Libraries

%description date-time

Run-Time support for Boost Date Time, set of date-time libraries based
on generic programming concepts.

%package filesystem
Summary: Run-Time component of boost filesystem library
Group: System Environment/Libraries
Requires: boost-system%{?_isa} = %{version}-%{release}

%description filesystem

Run-Time support for the Boost Filesystem Library, which provides
portable facilities to query and manipulate paths, files, and
directories.

%package graph
Summary: Run-Time component of boost graph library
Group: System Environment/Libraries
Requires: boost-regex%{?_isa} = %{version}-%{release}

%description graph

Run-Time support for the BGL graph library.  BGL interface and graph
components are generic, in the same sense as the the Standard Template
Library (STL).

%package iostreams
Summary: Run-Time component of boost iostreams library
Group: System Environment/Libraries

%description iostreams

Run-Time support for Boost.IOStreams, a framework for defining streams,
stream buffers and i/o filters.

%package locale
Summary: Run-Time component of boost locale library
Group: System Environment/Libraries
Requires: boost-chrono%{?_isa} = %{version}-%{release}
Requires: boost-system%{?_isa} = %{version}-%{release}
Requires: boost-thread%{?_isa} = %{version}-%{release}

%description locale

Run-Time support for Boost.Locale, a set of localization and Unicode
handling tools.

%package log
Summary: Run-Time component of boost logging library
Group: System Environment/Libraries

%description log

Boost.Log library aims to make logging significantly easier for the
application developer.  It provides a wide range of out-of-the-box
tools along with public interfaces for extending the library.

%package math
Summary: Math functions for boost TR1 library
Group: System Environment/Libraries

%description math

Run-Time support for C99 and C++ TR1 C-style Functions from math
portion of Boost.TR1.

%package program-options
Summary:  Run-Time component of boost program_options library
Group: System Environment/Libraries

%description program-options

Run-Time support of boost program options library, which allows program
developers to obtain (name, value) pairs from the user, via
conventional methods such as command line and configuration file.

%package python
Summary: Run-Time component of boost python library
Group: System Environment/Libraries

%description python

The Boost Python Library is a framework for interfacing Python and
C++. It allows you to quickly and seamlessly expose C++ classes
functions and objects to Python, and vice versa, using no special
tools -- just your C++ compiler.  This package contains run-time
support for Boost Python Library.

%package random
Summary: Run-Time component of boost random library
Group: System Environment/Libraries

%description random

Run-Time support for boost random library.

%package regex
Summary: Run-Time component of boost regular expression library
Group: System Environment/Libraries

%description regex

Run-Time support for boost regular expression library.

%package serialization
Summary: Run-Time component of boost serialization library
Group: System Environment/Libraries

%description serialization

Run-Time support for serialization for persistence and marshaling.

%package signals
Summary: Run-Time component of boost signals and slots library
Group: System Environment/Libraries

%description signals

Run-Time support for managed signals & slots callback implementation.

%package system
Summary: Run-Time component of boost system support library
Group: System Environment/Libraries

%description system

Run-Time component of Boost operating system support library, including
the diagnostics support that will be part of the C++0x standard
library.

%package test
Summary: Run-Time component of boost test library
Group: System Environment/Libraries

%description test

Run-Time support for simple program testing, full unit testing, and for
program execution monitoring.

%package thread
Summary: Run-Time component of boost thread library
Group: System Environment/Libraries
Requires: boost-system%{?_isa} = %{version}-%{release}

%description thread

Run-Time component Boost.Thread library, which provides classes and
functions for managing multiple threads of execution, and for
synchronizing data between the threads or providing separate copies of
data specific to individual threads.

%package timer
Summary: Run-Time component of boost timer library
Group: System Environment/Libraries
Requires: boost-chrono%{?_isa} = %{version}-%{release}
Requires: boost-system%{?_isa} = %{version}-%{release}

%description timer

"How long does my C++ code take to run?"
The Boost Timer library answers that question and does so portably,
with as little as one #include and one additional line of code.

%package wave
Summary: Run-Time component of boost C99/C++ pre-processing library
Group: System Environment/Libraries
Requires: boost-chrono%{?_isa} = %{version}-%{release}
Requires: boost-date-time%{?_isa} = %{version}-%{release}
Requires: boost-filesystem%{?_isa} = %{version}-%{release}
Requires: boost-system%{?_isa} = %{version}-%{release}
Requires: boost-thread%{?_isa} = %{version}-%{release}

%description wave

Run-Time support for the Boost.Wave library, a Standards conforming,
and highly configurable implementation of the mandated C99/C++
pre-processor functionality.

%package dev
Summary: The Boost C++ headers and shared development libraries
Group: Development/Libraries
Requires: boost%{?_isa} = %{version}-%{release}
Provides: boost-python-dev

# Odeint was shipped in Fedora 18, but later became part of Boost.
# Note we also obsolete odeint-doc down there.
# https://bugzilla.redhat.com/show_bug.cgi?id=892850
Provides: odeint = 2.2-5
Obsoletes: odeint < 2.2-5
Provides: odeint-dev = 2.2-5
Obsoletes: odeint-dev < 2.2-5

%description dev
Headers and shared object symbolic links for the Boost C++ libraries.

%package static
Summary: The Boost C++ static development libraries
Group: Development/Libraries
Requires: boost-dev%{?_isa} = %{version}-%{release}
Obsoletes: boost-dev-static < 1.34.1-14
Provides: boost-dev-static = %{version}-%{release}

%description static
Static Boost C++ libraries.

%package doc
Summary: HTML documentation for the Boost C++ libraries
Group: Documentation
%if 0%{?rhel} >= 6
BuildArch: noarch
%endif
Provides: boost-python-docs = %{version}-%{release}

# See the description above.
Provides: odeint-doc = 2.2-5
Obsoletes: odeint-doc < 2.2-5

%description doc
This package contains the documentation in the HTML format of the Boost C++
libraries. The documentation provides the same content as that on the Boost
web page (http://www.boost.org/doc/libs/1_40_0).

%package examples
Summary: Source examples for the Boost C++ libraries
Group: Documentation
%if 0%{?rhel} >= 6
BuildArch: noarch
%endif
Requires: boost-dev = %{version}-%{release}

%description examples
This package contains example source files distributed with boost.

%package build
Summary: Cross platform build system for C++ projects
Group: Development/Tools
Requires: boost-jam
BuildArch: noarch

%description build
Boost.Build is an easy way to build C++ projects, everywhere. You name
your pieces of executable and libraries and list their sources.  Boost.Build
takes care about compiling your sources with the right options,
creating static and shared libraries, making pieces of executable, and other
chores -- whether you're using GCC, MSVC, or a dozen more supported
C++ compilers -- on Windows, OSX, Linux and commercial UNIX systems.

%package jam
Summary: A low-level build tool
Group: Development/Tools

%description jam
Boost.Jam (BJam) is the low-level build engine tool for Boost.Build.
Historically, Boost.Jam is based on on FTJam and on Perforce Jam but has grown
a number of significant features and is now developed independently

%prep
%setup -q -n %{toplev_dirname}

# At least python2_version needs to be a macro so that it's visible in
# %%install as well.
%global python2_version %(/usr/bin/python2 %{SOURCE1})

%build
: PYTHON2_VERSION=%{python2_version}

# There are many strict aliasing warnings, and it's not feasible to go
# through them all at this time.
export RPM_OPT_FLAGS="$RPM_OPT_FLAGS -fno-strict-aliasing"

cat > ./tools/build/src/user-config.jam << "EOF"
import os ;
local RPM_OPT_FLAGS = [ os.environ RPM_OPT_FLAGS ] ;

using gcc : : : <compileflags>$(RPM_OPT_FLAGS) ;
EOF

./bootstrap.sh --with-toolset=gcc --with-icu

# N.B. When we build the following with PCH, parts of boost (math
# library in particular) end up being built second time during
# installation.  Unsure why that is, but all sub-builds need to be
# built with pch=off to avoid this.
#
# The "python=2.*" bit tells jam that we want to _also_ build 2.*, not
# just 3.*.  When omitted, it just builds for python 3 twice, once
# calling the library libboost_python and once libboost_python3.  I
# assume this is for backward compatibility for apps that are used to
# linking against -lboost_python, for when 2->3 transition is
# eventually done.

echo ============================= build serial ==================
./b2 -d+2 -q %{?_smp_mflags} \
	--without-mpi --without-graph_parallel --build-dir=serial \
	variant=release threading=multi debug-symbols=on pch=off \
	python=%{python2_version} stage

# See boost-1.54.0-thread-link_atomic.patch for where this file comes
# from.
if [ $(find serial -type f -name has_atomic_flag_lockfree \
		-print -quit | wc -l) -ne 0 ]; then
	DEF=D
else
	DEF=U
fi

m4 -${DEF}HAS_ATOMIC_FLAG_LOCKFREE -DVERSION=%{version} \
	%{SOURCE2} > $(basename %{SOURCE2})

# Build MPI parts of Boost with OpenMPI support

echo ============================= build Boost.Build ==================
(cd tools/build
 ./bootstrap.sh --with-toolset=gcc)

%check
:


%install
rm -rf $RPM_BUILD_ROOT
cd %{_builddir}/%{toplev_dirname}

echo ============================= install serial ==================
./b2 -d+2 -q %{?_smp_mflags} \
	--without-mpi --without-graph_parallel --build-dir=serial \
	--prefix=$RPM_BUILD_ROOT%{_prefix} \
	--libdir=$RPM_BUILD_ROOT%{_libdir} \
	variant=release threading=multi debug-symbols=on pch=off \
	python=%{python2_version} install

# Override DSO symlink with a linker script.  See the linker script
# itself for details of why we need to do this.
[ -f $RPM_BUILD_ROOT%{_libdir}/libboost_thread.so ] # Must be present
rm -f $RPM_BUILD_ROOT%{_libdir}/libboost_thread.so
install -p -m 644 $(basename %{SOURCE2}) $RPM_BUILD_ROOT%{_libdir}/

echo ============================= install Boost.Build ==================
(cd tools/build
 ./b2 --prefix=$RPM_BUILD_ROOT%{_prefix} install
 # Fix some permissions
 chmod -x $RPM_BUILD_ROOT%{_datadir}/boost-build/src/build/alias.py
 chmod +x $RPM_BUILD_ROOT%{_datadir}/boost-build/src/tools/doxproc.py
 # We don't want to distribute this
 rm -f $RPM_BUILD_ROOT%{_bindir}/b2
 # Not a real file
 rm -f $RPM_BUILD_ROOT%{_datadir}/boost-build/src/build/project.ann.py
 # Empty file
 rm -f $RPM_BUILD_ROOT%{_datadir}/boost-build/src/tools/doxygen/windows-paths-check.hpp
 # Install the manual page
 # FIXME: Missing??
 #%{__install} -p -m 644 v2/doc/bjam.1 -D $RPM_BUILD_ROOT%{_mandir}/man1/bjam.1
)

# Install documentation files (HTML pages) within the temporary place
echo ============================= install documentation ==================
# Prepare the place to temporary store the generated documentation
rm -rf %{boost_docdir} && %{__mkdir_p} %{boost_docdir}/html
DOCPATH=%{boost_docdir}
DOCREGEX='.*\.\(html?\|css\|png\|gif\)'

find libs doc more -type f -regex $DOCREGEX \
    | sed -n '/\//{s,/[^/]*$,,;p}' \
    | sort -u > tmp-doc-directories

sed "s:^:$DOCPATH/:" tmp-doc-directories \
    | xargs -P 0 --no-run-if-empty %{__install} -d

cat tmp-doc-directories | while read tobeinstalleddocdir; do
    find $tobeinstalleddocdir -mindepth 1 -maxdepth 1 -regex $DOCREGEX \
    | xargs -P 0 %{__install} -p -m 644 -t $DOCPATH/$tobeinstalleddocdir
done
rm -f tmp-doc-directories
%{__install} -p -m 644 -t $DOCPATH LICENSE_1_0.txt index.htm index.html boost.png rst.css boost.css

echo ============================= install examples ==================
# Fix a few non-standard issues (DOS and/or non-UTF8 files)
sed -i -e 's/\r//g' libs/geometry/example/ml02_distance_strategy.cpp
for tmp_doc_file in flyweight/example/Jamfile.v2 \
 format/example/sample_new_features.cpp multi_index/example/Jamfile.v2 \
 multi_index/example/hashed.cpp serialization/example/demo_output.txt \
 test/example/cla/wide_string.cpp
do
  mv libs/${tmp_doc_file} libs/${tmp_doc_file}.iso8859
  iconv -f ISO8859-1 -t UTF8 < libs/${tmp_doc_file}.iso8859 > libs/${tmp_doc_file}
  touch -r libs/${tmp_doc_file}.iso8859 libs/${tmp_doc_file}
  rm -f libs/${tmp_doc_file}.iso8859
done

# Prepare the place to temporary store the examples
rm -rf %{boost_examplesdir} && mkdir -p %{boost_examplesdir}/html
EXAMPLESPATH=%{boost_examplesdir}
find libs -type d -name example -exec find {} -type f \; \
    | sed -n '/\//{s,/[^/]*$,,;p}' \
    | sort -u > tmp-doc-directories
sed "s:^:$EXAMPLESPATH/:" tmp-doc-directories \
    | xargs -P 0 --no-run-if-empty %{__install} -d
rm -f tmp-doc-files-to-be-installed && touch tmp-doc-files-to-be-installed
cat tmp-doc-directories | while read tobeinstalleddocdir
do
  find $tobeinstalleddocdir -mindepth 1 -maxdepth 1 -type f \
    >> tmp-doc-files-to-be-installed
done
cat tmp-doc-files-to-be-installed | while read tobeinstalledfiles
do
  if test -s $tobeinstalledfiles
  then
    tobeinstalleddocdir=`dirname $tobeinstalledfiles`
    %{__install} -p -m 644 -t $EXAMPLESPATH/$tobeinstalleddocdir $tobeinstalledfiles
  fi
done
rm -f tmp-doc-files-to-be-installed
rm -f tmp-doc-directories
%{__install} -p -m 644 -t $EXAMPLESPATH LICENSE_1_0.txt

%clean
rm -rf $RPM_BUILD_ROOT


# MPI subpackages don't need the ldconfig magic.  They are hidden by
# default, in MPI back-end-specific directory, and only show to the
# user after the relevant environment module has been loaded.
# rpmlint will report that as errors, but it is fine.

%post atomic -p /sbin/ldconfig

%postun atomic -p /sbin/ldconfig

%post chrono -p /sbin/ldconfig

%postun chrono -p /sbin/ldconfig

%post container -p /sbin/ldconfig

%postun container -p /sbin/ldconfig

%post context -p /sbin/ldconfig

%postun context -p /sbin/ldconfig

%post coroutine -p /sbin/ldconfig

%postun coroutine -p /sbin/ldconfig

%post date-time -p /sbin/ldconfig

%postun date-time -p /sbin/ldconfig

%post filesystem -p /sbin/ldconfig

%postun filesystem -p /sbin/ldconfig

%post graph -p /sbin/ldconfig

%postun graph -p /sbin/ldconfig

%post iostreams -p /sbin/ldconfig

%postun iostreams -p /sbin/ldconfig

%post locale -p /sbin/ldconfig

%postun locale -p /sbin/ldconfig

%post log -p /sbin/ldconfig

%postun log -p /sbin/ldconfig

%post math -p /sbin/ldconfig

%postun math -p /sbin/ldconfig

%post program-options -p /sbin/ldconfig

%postun program-options -p /sbin/ldconfig

%post python -p /sbin/ldconfig

%postun python -p /sbin/ldconfig

%post random -p /sbin/ldconfig

%postun random -p /sbin/ldconfig

%post regex -p /sbin/ldconfig

%postun regex -p /sbin/ldconfig

%post serialization -p /sbin/ldconfig

%postun serialization -p /sbin/ldconfig

%post signals -p /sbin/ldconfig

%postun signals -p /sbin/ldconfig

%post system -p /sbin/ldconfig

%postun system -p /sbin/ldconfig

%post test -p /sbin/ldconfig

%postun test -p /sbin/ldconfig

%post thread -p /sbin/ldconfig

%postun thread -p /sbin/ldconfig

%post timer -p /sbin/ldconfig

%postun timer -p /sbin/ldconfig

%post wave -p /sbin/ldconfig

%postun wave -p /sbin/ldconfig



%files
%defattr(-, root, root, -)
%doc LICENSE_1_0.txt

%files atomic
%defattr(-, root, root, -)
%doc LICENSE_1_0.txt
%{_libdir}/libboost_atomic.so.%{sonamever}

%files chrono
%defattr(-, root, root, -)
%doc LICENSE_1_0.txt
%{_libdir}/libboost_chrono.so.%{sonamever}

%files container
%defattr(-, root, root, -)
%doc LICENSE_1_0.txt
%{_libdir}/libboost_container.so.%{sonamever}

%files context
%defattr(-, root, root, -)
%doc LICENSE_1_0.txt
%{_libdir}/libboost_context.so.%{sonamever}

%files coroutine
%defattr(-, root, root, -)
%doc LICENSE_1_0.txt
%{_libdir}/libboost_coroutine.so.%{sonamever}

%files date-time
%defattr(-, root, root, -)
%doc LICENSE_1_0.txt
%{_libdir}/libboost_date_time.so.%{sonamever}

%files filesystem
%defattr(-, root, root, -)
%doc LICENSE_1_0.txt
%{_libdir}/libboost_filesystem.so.%{sonamever}

%files graph
%defattr(-, root, root, -)
%doc LICENSE_1_0.txt
%{_libdir}/libboost_graph.so.%{sonamever}

%files iostreams
%defattr(-, root, root, -)
%doc LICENSE_1_0.txt
%{_libdir}/libboost_iostreams.so.%{sonamever}

%files locale
%defattr(-, root, root, -)
%doc LICENSE_1_0.txt
%{_libdir}/libboost_locale.so.%{sonamever}

%files log
%defattr(-, root, root, -)
%doc LICENSE_1_0.txt
%{_libdir}/libboost_log.so.%{sonamever}
%{_libdir}/libboost_log_setup.so.%{sonamever}

%files math
%defattr(-, root, root, -)
%doc LICENSE_1_0.txt
%{_libdir}/libboost_math_c99.so.%{sonamever}
%{_libdir}/libboost_math_c99f.so.%{sonamever}
%{_libdir}/libboost_math_c99l.so.%{sonamever}
%{_libdir}/libboost_math_tr1.so.%{sonamever}
%{_libdir}/libboost_math_tr1f.so.%{sonamever}
%{_libdir}/libboost_math_tr1l.so.%{sonamever}

%files test
%defattr(-, root, root, -)
%doc LICENSE_1_0.txt
%{_libdir}/libboost_prg_exec_monitor.so.%{sonamever}
%{_libdir}/libboost_unit_test_framework.so.%{sonamever}

%files program-options
%defattr(-, root, root, -)
%doc LICENSE_1_0.txt
%{_libdir}/libboost_program_options.so.%{sonamever}

%files python
%defattr(-, root, root, -)
%doc LICENSE_1_0.txt
%{_libdir}/libboost_python.so.%{sonamever}

%files random
%defattr(-, root, root, -)
%doc LICENSE_1_0.txt
%{_libdir}/libboost_random.so.%{sonamever}

%files regex
%defattr(-, root, root, -)
%doc LICENSE_1_0.txt
%{_libdir}/libboost_regex.so.%{sonamever}

%files serialization
%defattr(-, root, root, -)
%doc LICENSE_1_0.txt
%{_libdir}/libboost_serialization.so.%{sonamever}
%{_libdir}/libboost_wserialization.so.%{sonamever}

%files signals
%defattr(-, root, root, -)
%doc LICENSE_1_0.txt
%{_libdir}/libboost_signals.so.%{sonamever}

%files system
%defattr(-, root, root, -)
%doc LICENSE_1_0.txt
%{_libdir}/libboost_system.so.%{sonamever}

%files thread
%defattr(-, root, root, -)
%doc LICENSE_1_0.txt
%{_libdir}/libboost_thread.so.%{sonamever}

%files timer
%defattr(-, root, root, -)
%doc LICENSE_1_0.txt
%{_libdir}/libboost_timer.so.%{sonamever}

%files wave
%defattr(-, root, root, -)
%doc LICENSE_1_0.txt
%{_libdir}/libboost_wave.so.%{sonamever}

%files doc
%defattr(-, root, root, -)
%doc %{boost_docdir}/*

%files examples
%defattr(-, root, root, -)
%doc %{boost_examplesdir}/*

%files dev
%defattr(-, root, root, -)
%doc LICENSE_1_0.txt
%{_includedir}/%{name}
%{_libdir}/libboost_atomic.so
%{_libdir}/libboost_chrono.so
%{_libdir}/libboost_container.so
%{_libdir}/libboost_context.so
%{_libdir}/libboost_coroutine.so
%{_libdir}/libboost_date_time.so
%{_libdir}/libboost_filesystem.so
%{_libdir}/libboost_graph.so
%{_libdir}/libboost_iostreams.so
%{_libdir}/libboost_locale.so
%{_libdir}/libboost_log.so
%{_libdir}/libboost_log_setup.so
%{_libdir}/libboost_math_tr1.so
%{_libdir}/libboost_math_tr1f.so
%{_libdir}/libboost_math_tr1l.so
%{_libdir}/libboost_math_c99.so
%{_libdir}/libboost_math_c99f.so
%{_libdir}/libboost_math_c99l.so
%{_libdir}/libboost_prg_exec_monitor.so
%{_libdir}/libboost_unit_test_framework.so
%{_libdir}/libboost_program_options.so
%{_libdir}/libboost_python.so
%{_libdir}/libboost_random.so
%{_libdir}/libboost_regex.so
%{_libdir}/libboost_serialization.so
%{_libdir}/libboost_wserialization.so
%{_libdir}/libboost_signals.so
%{_libdir}/libboost_system.so
%{_libdir}/libboost_thread.so
%{_libdir}/libboost_timer.so
%{_libdir}/libboost_wave.so

%files static
%defattr(-, root, root, -)
%doc LICENSE_1_0.txt
%{_libdir}/*.a

%files build
%defattr(-, root, root, -)
%doc LICENSE_1_0.txt
%{_datadir}/boost-build/

%files jam
%defattr(-, root, root, -)
%doc LICENSE_1_0.txt
%{_bindir}/bjam
#%{_mandir}/man1/bjam.1*

%changelog
* Mon Apr 27 2015 Daniel Vrátil <dvratil@redhat.com> - 1.57.0-1
- Initial version (forked from Fedora)
