#
# Conditional build:
%bcond_without	dist_kernel	# without distribution kernel
%bcond_without	kernel		# without kernel modules
%bcond_without	userspace	# without userspace packages
#
Summary:	Linux kernel module for network shaping
Summary(pl):	Modu³ j±dra Linuksa do ograniczania pasma w sieci
Name:		rshaper
Version:	031217
Epoch:		1
%define rel 1
Release:	%{rel}
License:	GPL
Group:		Base/Kernel
#SourceX:	http://ar.linux.it/pub/rshaper/%{name}-%{version}.tar.gz
Source0:	http://ar.linux.it/pub/rshaper/CVS-snapshots/%{name}-snapshot-%{version}.tar.gz
# Source0-md5:	bfaecb170fc2fae24f2ae4109d7bceaf
Patch0:		%{name}-Makefile.patch
URL:		http://ar.linux.it/software/#rshaper
%if %{with kernel} && %{with dist_kernel}
BuildRequires:	kernel-headers
BuildRequires:	%{kgcc_package}
%endif
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
rshaper is a module for versions 2.0, 2.2 and 2.4 of the Linux kernel,
it is meant to limit the incoming bandwidth for packets aimed at
different hosts/ports. 

This package contains userspace utility to control rshaper module.

%description -l pl
rshaper to modu³ dla j±der Linuksa w wersjach 2.0, 2.2 i 2.4, s³u¿±cy
do ograniczania pasma przychodz±cych pakietów przeznaczonych dla
ró¿nych hostów/portów.

Ten pakiet zawiera narzêdzie do sterowania modu³em rshaper.

%package -n kernel-misc-rshaper
Summary:	Linux kernel module for network shaping
Summary(pl):	Modu³ j±dra Linuksa do ograniczania pasma w sieci
Group:		Base/Kernel
Release:	%{rel}@%{_kernel_ver_str}
%{?with_dist_kernel:%requires_releq_kernel_up}
Requires(post,postun):	/sbin/depmod
Requires:	%{name} = %{version}-%{rel}

%description -n kernel-misc-rshaper
Linux kernel module for network shaping.

%description -n kernel-misc-rshaper -l pl
Modu³ j±dra Linuksa do ograniczania pasma w sieci.

%package -n kernel-smp-misc-rshaper
Summary:	Linux kernel module for network shaping
Summary(pl):	Modu³ j±dra Linuksa do ograniczania pasma w sieci
Group:		Base/Kernel
Release:	%{rel}@%{_kernel_ver_str}
%{?with_dist_kernel:%requires_releq_kernel_smp}
Requires(post,postun):	/sbin/depmod
Requires:	%{name} = %{version}-%{rel}

%description -n kernel-smp-misc-rshaper
Linux kernel module for network shaping.

%description -n kernel-smp-misc-rshaper -l pl
Modu³ j±dra Linuksa do ograniczania pasma w sieci.

%prep
%setup -q -n %{name}-snapshot-%{version}
%patch0 -p1

%build
%if %{with userspace}
%{__make} rshaperctl \
	CC="%{__cc}" \
	CFLAGS="%{rpmcflags} -Wall"
%endif

%if %{with kernel}
%{__make} rshaper.o \
	CC="%{kgcc}" \
	CFLAGS="%{rpmcflags} -D__SMP__ -Wall -I%{_kernelsrcdir}/include %{?debug:-DRSHAPER_DEBUG}"
mv -f rshaper.o rshaper-smp.o
%{__make} rshaper.o \
	CC="%{kgcc}" \
	CFLAGS="%{rpmcflags} -Wall -I%{_kernelsrcdir}/include %{?debug:-DRSHAPER_DEBUG}"
%endif

%install
rm -rf $RPM_BUILD_ROOT

%if %{with userspace}
install -d $RPM_BUILD_ROOT{%{_sbindir},%{_mandir}/man8}
install rshaperctl $RPM_BUILD_ROOT%{_sbindir}
install rshaperctl.8 $RPM_BUILD_ROOT%{_mandir}/man8
%endif

%if %{with kernel}
install -d $RPM_BUILD_ROOT/lib/modules/%{_kernel_ver}{,smp}/misc
install rshaper.o $RPM_BUILD_ROOT/lib/modules/%{_kernel_ver}/misc
install rshaper-smp.o $RPM_BUILD_ROOT/lib/modules/%{_kernel_ver}smp/misc/rshaper.o
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%post	-n kernel-misc-rshaper
%depmod %{_kernel_ver}

%postun -n kernel-misc-rshaper
%depmod %{_kernel_ver}

%post	-n kernel-smp-misc-rshaper
%depmod %{_kernel_ver}smp

%postun -n kernel-smp-misc-rshaper
%depmod %{_kernel_ver}smp

%if %{with userspace}
%files
%defattr(644,root,root,755)
%doc README README.locks TODO
%attr(755,root,root) %{_sbindir}/*
%{_mandir}/man8/*

%endif

%if %{with kernel}
%files -n kernel-misc-rshaper
%defattr(644,root,root,755)
/lib/modules/%{_kernel_ver}/misc/rshaper.o*

%files -n kernel-smp-misc-rshaper
%defattr(644,root,root,755)
/lib/modules/%{_kernel_ver}smp/misc/rshaper.o*
%endif
