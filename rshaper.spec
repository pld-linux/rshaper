# TODO: optflags, standard UP/SMP scheme
Summary:	Linux kernel module for network shaping
Summary(pl):	Modu³ j±dra Linuksa do ograniczania pasma w sieci
Name:		rshaper
Version:	2.01
Release:	2
License:	GPL
Group:		Base/Kernel
Source0:	http://ar.linux.it/pub/rshaper/%{name}-%{version}.tar.gz
# Source0-md5:	a246d0364e5ca3de8199a0f83b758534
Patch0:		%{name}-Makefile.patch
URL:		http://ar.linux.it/software/#rshaper
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This is a module for versions 2.0, 2.2 and 2.4 of the Linux kernel, it
is meant to limit the incoming bandwidth for packets aimed at
different hosts. 

%description -l pl
Ten pakiet zawiera modu³ dla j±der Linuksa w wersjach 2.0, 2.2 i 2.4,
s³u¿±cy do ograniczania pasma przychodz±cych pakietów przeznaczonych
dla ró¿nych hostów.

%prep
%setup -q
%patch0 -p1

%build
%{__make} clean
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT \
	VERSION="%{_kernel_ver}"


%post
/sbin/depmod
%postun
/sbin/depmod

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc README README.locks TODO
%attr(755,root,root) %{_sbindir}/*
%{_mandir}/man8/*
/lib/modules/%{_kernel_ver}/misc/*
