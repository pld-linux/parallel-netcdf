#
# Conditional build:
%bcond_without	apidocs		# API documentation
%bcond_without	static_libs	# static library
#
Summary:	Parallel netCDF (PnetCDF) library
Summary(pl.UTF-8):	Biblioteka zrównoleglona netCDF (PnetCDF)
Name:		parallel-netcdf
Version:	1.12.0
Release:	1
License:	BSD-like
Group:		Libraries
#Source0Download: http://cucis.ece.northwestern.edu/projects/PnetCDF/download.html
Source0:	http://cucis.ece.northwestern.edu/projects/PnetCDF/Release/pnetcdf-%{version}.tar.gz
# Source0-md5:	67ba3266da3c6050ba3dc042d67551d7
Patch0:		%{name}-sh.patch
URL:		https://trac.mcs.anl.gov/projects/parallel-netcdf
BuildRequires:	autoconf >= 2.69
BuildRequires:	automake >= 1:1.13
BuildRequires:	gcc-fortran
BuildRequires:	libstdc++-devel
BuildRequires:	libtool >= 2:2.4.2
# mpicc and co.
BuildRequires:	mpich-devel
BuildRequires:	m4
%if %{with apidocs}
BuildRequires:	doxygen
BuildRequires:	ghostscript
BuildRequires:	texlive-latex
%endif
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Parallel netCDF (PnetCDF) is a library providing high-performance
parallel I/O while still maintaining file-format compatibility with
Unidata's NetCDF, specifically the classic CDF 1, 2, and 5 formats.
Although NetCDF supports parallel I/O starting from version 4, it is
built on top of HDF5 and thus its parallel feature requires files in
HDF5 format. PnetCDF is currently the only option for parallel I/O on
files in classic formats.

%description -l pl.UTF-8
Parallel netCDF (PnetCDF) to biblioteka zapewniająca bardzo wydajne,
równoległe operacje we/wy, zachowując zgodność z formatem plików
Unidata NetCDF, w szczególności klasycznych formatach CDF 1, 2, 5.
Mimo że NetCDF obsługuje równoległe operacje we/wy począwszy od wersji
4, ale w oparciu o HDF5, więc opcja zrównoleglenia wymaga plików w
formacie HDF5. PnetCDF to obecnie jedyna możliwość zrównoleglenia
we/wy dla plików w klasycznych formatach.

%package devel
Summary:	Header files for PnetCDF library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki PnetCDF
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	mpich-devel

%description devel
Header files for PnetCDF library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki PnetCDF.

%package static
Summary:	Static PnetCDF library
Summary(pl.UTF-8):	Statyczna biblioteka PnetCDF
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static PnetCDF library.

%description static -l pl.UTF-8
Statyczna biblioteka PnetCDF.

%package apidocs
Summary:	API documentation for PnetCDF library
Summary(pl.UTF-8):	Dokumentacja API biblioteki PnetCDF
Group:		Documentation
%if "%{_rpmversion}" >= "5"
BuildArch:	noarch
%endif

%description apidocs
API documentation for PnetCDF library.

%description apidocs -l pl.UTF-8
Dokumentacja API biblioteki PnetCDF.

%prep
%setup -q -n pnetcdf-%{version}
%patch0 -p1

%build
%{__libtoolize}
%{__aclocal} -I m4
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	%{?with_apidocs:--enable-doxygen} \
	--disable-silent-rules \
	--enable-shared \
	%{!?with_static_libs:--disable-static}
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

# .la kept because of MPI dependencies

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS COPYRIGHT CREDITS README RELEASE_NOTES doc/README.{LINUX,consistency,large_files}
%attr(755,root,root) %{_bindir}/cdfdiff
%attr(755,root,root) %{_bindir}/ncmpidiff
%attr(755,root,root) %{_bindir}/ncmpidump
%attr(755,root,root) %{_bindir}/ncmpigen
%attr(755,root,root) %{_bindir}/ncoffsets
%attr(755,root,root) %{_bindir}/ncvalidator
%attr(755,root,root) %{_bindir}/pnetcdf_version
%attr(755,root,root) %{_libdir}/libpnetcdf.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libpnetcdf.so.4
%{_mandir}/man1/cdfdiff.1*
%{_mandir}/man1/ncmpidiff.1*
%{_mandir}/man1/ncmpidump.1*
%{_mandir}/man1/ncmpigen.1*
%{_mandir}/man1/ncoffsets.1*
%{_mandir}/man1/ncvalidator.1*
%{_mandir}/man1/pnetcdf_version.1*

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/pnetcdf-config
%attr(755,root,root) %{_libdir}/libpnetcdf.so
%{_libdir}/libpnetcdf.la
%{_includedir}/pnetcdf.h
%{_includedir}/pnetcdf
%{_includedir}/pnetcdf.inc
%{_includedir}/pnetcdf.mod
%{_pkgconfigdir}/pnetcdf.pc
%{_mandir}/man3/pnetcdf.3*
%{_mandir}/man3/pnetcdf_f77.3*
%{_mandir}/man3/pnetcdf_f90.3*

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libpnetcdf.a
%endif

%if %{with apidocs}
%files apidocs
%defattr(644,root,root,755)
%doc doc/pnetcdf-api/pnetcdf-api.pdf
%endif
