Name:           xcb-util-wm
Version:        0.4.1
Release:        1%{?dist}
Summary:        Client and window-manager helper library on top of libxcb
Group:          System Environment/Libraries
License:        MIT
URL:            http://xcb.freedesktop.org
Source0:        http://xcb.freedesktop.org/dist/%{name}-%{version}.tar.bz2

BuildRequires:  freedesktop-sdk-base
BuildRequires:  libxcb-dev

BuildRequires:  xcb-util-dev

%description
XCB util-wm module provides the following libraries:

  - ewmh: Both client and window-manager helpers for EWMH.
  - icccm: Both client and window-manager helpers for ICCCM.


%package        dev
Summary:        Development and header files for xcb-util-vm
Group:          System Environment/Libraries
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description    dev
Development files for xcb-util-wm.


%prep
%setup -q


%build
%configure --with-pic --disable-static --disable-silent-rules
make %{?_smp_mflags}


%check
make check


%install
make install DESTDIR=%{buildroot} INSTALL="install -p"
rm %{buildroot}%{_libdir}/*.la


%post -p /sbin/ldconfig


%postun -p /sbin/ldconfig


%files
%doc README COPYING
%{_libdir}/*.so.*


%files dev
%doc NEWS
%{_libdir}/pkgconfig/*.pc
%{_libdir}/*.so
%{_includedir}/xcb/*.h


%changelog
* Wed Oct 22 2014 Thomas Moschny <thomas.moschny@gmx.de> - 0.4.1-5
- Include COPYING.

* Mon Aug 18 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Thu Apr 17 2014 Thomas Moschny <thomas.moschny@gmx.de> - 0.4.1-2
- Disable silent build.

* Wed Apr 16 2014 Hans de Goede <hdegoede@redhat.com> - 0.4.1-1
- Update to 0.4.1 (rhbz#1059674)

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.9-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Fri Feb 15 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.9-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Mon Aug 20 2012 Thomas Moschny <thomas.moschny@gmx.de> - 0.3.9-1
- Update to 0.3.9.

* Sun Jul 22 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.8-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Apr  5 2012 Thomas Moschny <thomas.moschny@gmx.de> - 0.3.8-2
- Specfile cleanups as suggested in the review.
- Remove unneeded BR on pkgconfig.
- Remove unneeded chrpath call.

* Mon Dec  5 2011 Thomas Moschny <thomas.moschny@gmx.de> - 0.3.8-1
- New package.

