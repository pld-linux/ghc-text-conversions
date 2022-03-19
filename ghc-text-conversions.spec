#
# Conditional build:
%bcond_without	prof	# profiling library
#
%define		pkgname	text-conversions
Summary:	Safe conversions between textual types
Name:		ghc-%{pkgname}
Version:	0.3.0
Release:	2
License:	ISC
Group:		Development/Languages
#Source0Download: http://hackage.haskell.org/package/text-conversions
Source0:	http://hackage.haskell.org/package/%{pkgname}-%{version}/%{pkgname}-%{version}.tar.gz
# Source0-md5:	688bc606dac77ef155782582a7bffe9f
URL:		http://hackage.haskell.org/package/text-conversions
BuildRequires:	ghc >= 6.12.3
BuildRequires:	ghc-base16-bytestring
BuildRequires:	ghc-base64-bytestring
BuildRequires:	ghc-errors
%if %{with prof}
BuildRequires:	ghc-prof
BuildRequires:	ghc-base16-bytestring-prof
BuildRequires:	ghc-base64-bytestring-prof
BuildRequires:	ghc-errors-prof
%endif
BuildRequires:	rpmbuild(macros) >= 1.608
%requires_eq	ghc
Requires(post,postun):	/usr/bin/ghc-pkg
Requires:	ghc-base16-bytestring
Requires:	ghc-base64-bytestring
Requires:	ghc-errors
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

# debuginfo is not useful for ghc
%define		_enable_debug_packages	0

# don't compress haddock files
%define		_noautocompressdoc	*.haddock

%description
This is a small library to ease the pain when converting between
the many different string types in Haskell.

%package prof
Summary:	Profiling %{pkgname} library for GHC
Summary(pl.UTF-8):	Biblioteka profilująca %{pkgname} dla GHC
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	ghc-base16-bytestring-prof
Requires:	ghc-base64-bytestring-prof
Requires:	ghc-errors-prof

%description prof
Profiling %{pkgname} library for GHC.  Should be installed when
GHC's profiling subsystem is needed.

%description prof -l pl.UTF-8
Biblioteka profilująca %{pkgname} dla GHC. Powinna być zainstalowana
kiedy potrzebujemy systemu profilującego z GHC.

%prep
%setup -q -n %{pkgname}-%{version}

%build
runhaskell Setup.hs configure -v2 \
	%{?with_prof:--enable-library-profiling} \
	--prefix=%{_prefix} \
	--libdir=%{_libdir} \
	--libexecdir=%{_libexecdir} \
	--docdir=%{_docdir}/%{name}-%{version}

runhaskell Setup.hs build
runhaskell Setup.hs haddock --executables

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_libdir}/%{ghcdir}/package.conf.d

runhaskell Setup.hs copy --destdir=$RPM_BUILD_ROOT

# work around automatic haddock docs installation
%{__rm} -rf %{name}-%{version}-doc
cp -a $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version} %{name}-%{version}-doc
%{__rm} -r $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version}

runhaskell Setup.hs register \
	--gen-pkg-config=$RPM_BUILD_ROOT%{_libdir}/%{ghcdir}/package.conf.d/%{pkgname}.conf

%clean
rm -rf $RPM_BUILD_ROOT

%post
%ghc_pkg_recache

%postun
%ghc_pkg_recache

%files
%defattr(644,root,root,755)
%doc CHANGELOG.md README.md %{name}-%{version}-doc/*
%{_libdir}/%{ghcdir}/package.conf.d/%{pkgname}.conf
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/*.so
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/*.a
%exclude %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/*_p.a

%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/Text
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/Text/*.hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/Text/*.dyn_hi

%if %{with prof}
%files prof
%defattr(644,root,root,755)
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/*_p.a
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/Text/*.p_hi
%endif
