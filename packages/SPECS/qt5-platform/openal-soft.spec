Name:           openal-soft
Version:        1.16.0
Release:        1%{?dist}
Summary:        Open Audio Library

Group:          System Environment/Libraries
License:        LGPLv2+
URL:            http://kcat.strangesoft.net/openal.html
Source0:        http://kcat.strangesoft.net/openal-releases/openal-soft-%{version}.tar.bz2
Patch0:         openal-soft-arm_neon-only-for-32bit.patch

BuildRequires:  qt5-sdk-base

BuildRequires:  alsa-lib-dev
BuildRequires:  portaudio-dev

Provides:       openal = %{version}

%description
OpenAL Soft is a cross-platform software implementation of the OpenAL 3D
audio API. It's built off of the open-sourced Windows version available
originally from the SVN repository at openal.org. OpenAL provides
capabilities for playing audio in a virtual 3d environment. Distance
attenuation, doppler shift, and directional sound emitters are among
the features handled by the API. More advanced effects, including air
absorption, low-pass filters, and reverb, are available through the
EFX extension. It also facilitates streaming audio, multi-channel buffers,
and audio capture.

%package        dev
Summary:        Development files for %{name}
Group:          Development/Libraries
Requires:       %{name}%{?_isa} = %{version}-%{release}
Obsoletes:      openal-dev <= 0.0.10
Provides:       openal-dev = %{version}

%description    dev
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%prep
%setup -q
%patch0 -p1

%build
%{cmake} .
make %{?_smp_mflags}

%install
make install DESTDIR=%{buildroot}
find %{buildroot} -name '*.la' -exec rm -f {} ';'
install -Dpm644 alsoftrc.sample %{buildroot}%{_sysconfdir}/openal/alsoft.conf

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%doc COPYING
%{_bindir}/openal-info
%{_libdir}/libopenal.so.*
%dir %{_sysconfdir}/openal
%config(noreplace) %{_sysconfdir}/openal/alsoft.conf
%dir %{_datarootdir}/openal
%{_datarootdir}/openal/alsoftrc.sample
%dir %{_datarootdir}/openal/hrtf
%{_datarootdir}/openal/hrtf/default-44100.mhr
%{_datarootdir}/openal/hrtf/default-48000.mhr

%files dev
%{_bindir}/makehrtf
%{_includedir}/*
%{_libdir}/libopenal.so
%{_libdir}/pkgconfig/openal.pc

%changelog
* Mon Apr 20 2015 Daniel Vrátil <dvratil@redhat.com> - 1.16.0-1
- Initial version (forked from Fedora, minus qt)
