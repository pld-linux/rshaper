Summary:	Kernel module for network shaping.
Name:		rshaper
Version:	2.01
Release:	1
License:	GPL
Group:		Base/Kernel
Source0:	http://ar.linux.it/pub/rshaper/%{name}-%{version}.tar.gz
# Source0-md5:	a246d0364e5ca3de8199a0f83b758534
Patch0:		%{name}-Makefile.patch
URL:		http://ar.linux.it/software/#rshaper
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This is a module for versions 2.0, 2.2 and 2.4 of the Linux kernel, it
is  meant  to  limit  the  incoming bandwidth  for  packets  aimed  at
different  hosts. 


%prep
%setup -q -n %{name}-%{version}
%patch0 -p1

%build
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
# create directories if necessary
#install -d $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT \
	VERSION="%{_kernel_ver}"

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc README README.locks TODO
%attr(755,root,root) %{_sbindir}/*
%{_datadir}/man/man8/*
/lib/modules/%{_kernel_ver}/misc/*
