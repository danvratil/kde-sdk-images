# Place rpm-macros into proper location.
%global macrosdir %(d=%{_rpmconfigdir}/macros.d; [ -d $d ] || d=%{_sysconfdir}/rpm; echo $d)

Name:			fdupes
Version:		1.51
Release:		1%{?dist}
Summary:		Finds duplicate files in a given set of directories
%{?el5:Group:		Applications/File}

License:		MIT
URL:			https://code.google.com/p/fdupes/
Source0:		https://fdupes.googlecode.com/files/%{name}-%{version}.tar.gz
Source1:		macros.fdupes

Patch0:			fdupes-1.51-destdir.patch
# http://bugs.debian.org/353789
Patch1:			fdupes-1.51-typo.patch
# Fix CVE
Patch2:			fdupes-1.51-check-permissions.patch
# Apply proper LDFLAGS
Patch3:			fdupes-1.51-obey-ldflags.patch

%{?el5:BuildRoot:	%(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)}

%description
FDUPES is a program for identifying duplicate files residing within specified
directories.


%prep
%setup -q
%patch2 -p1 -b .cve
%patch0 -p1 -b .destdir
%patch1 -p1 -b .typo
%patch3 -p1 -b .ldflags


%build
make	%{?_smp_mflags}				\
	COMPILER_OPTIONS="%{?optflags}"		\
	LDFLAGS="%{?__global_ldflags}"


%check
./%{name} testdir
./%{name} --omitfirst testdir
./%{name} --recurse testdir
./%{name} --size testdir


%install
%{?el5:rm -rf %{buildroot}}
make install	INSTALL="%{__install} -p"	\
		BIN_DIR=%{_bindir}		\
		MAN_BASE_DIR=%{_mandir}		\
		DESTDIR=%{buildroot}

mkdir -p %{buildroot}%{macrosdir}
install -pm 0644 %{SOURCE1} %{buildroot}%{macrosdir}


%clean
%{?el5:rm -rf %{buildroot}}


%files
%doc CHANGES CONTRIBUTORS README TODO
%doc %{_mandir}/man1/%{name}.1*
%{_bindir}/%{name}
%{macrosdir}/macros.fdupes


%changelog
* Fri Apr 24 2015 Daniel Vrátil <dvratil@redhat.com> - 1.51-1
- Initial version (forked from Fedora)

