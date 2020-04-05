# Define the kmod package name here.
%define kmod_name ar5523

# If kversion isn't defined on the rpmbuild line, define it here.
%{!?kversion: %define kversion 3.10.0-1127.el7.%{_target_cpu}}

Name:    %{kmod_name}-kmod
Version: 0.0
Release: 10%{?dist}
Group:   System Environment/Kernel
License: GPLv2
Summary: %{kmod_name} kernel module(s)
URL:     http://www.kernel.org/

BuildRequires: perl
BuildRequires: redhat-rpm-config
ExclusiveArch: x86_64

# Sources.
Source0:  %{kmod_name}-%{version}.tar.gz
Source5:  GPL-v2.0.txt
Source10: kmodtool-%{kmod_name}-el7.sh

# Magic hidden here.
%{expand:%(sh %{SOURCE10} rpmtemplate %{kmod_name} %{kversion} "")}

# Disable the building of the debug package(s).
%define debug_package %{nil}

%description
This package provides the %{kmod_name} kernel module(s).
It is built to depend upon the specific ABI provided by a range of releases
of the same variant of the Linux kernel and not on any one specific build.

%prep
%setup -q -n %{kmod_name}-%{version}
echo "override %{kmod_name} * weak-updates/%{kmod_name}" > kmod-%{kmod_name}.conf
echo "override ath * weak-updates/%{kmod_name}" >> kmod-%{kmod_name}.conf

%build
KSRC=%{_usrsrc}/kernels/%{kversion}
%{__make} -C "${KSRC}" %{?_smp_mflags} modules M=$PWD

%install
%{__install} -d %{buildroot}/lib/modules/%{kversion}/extra/%{kmod_name}/
%{__install} ath.ko %{buildroot}/lib/modules/%{kversion}/extra/%{kmod_name}/
%{__install} %{kmod_name}/%{kmod_name}.ko %{buildroot}/lib/modules/%{kversion}/extra/%{kmod_name}/
%{__install} -d %{buildroot}%{_sysconfdir}/depmod.d/
%{__install} kmod-%{kmod_name}.conf %{buildroot}%{_sysconfdir}/depmod.d/
%{__install} -d %{buildroot}%{_defaultdocdir}/kmod-%{kmod_name}-%{version}/
%{__install} %{SOURCE5} %{buildroot}%{_defaultdocdir}/kmod-%{kmod_name}-%{version}/

# strip the modules(s)
find %{buildroot} -type f -name \*.ko -exec %{__strip} --strip-debug \{\} \;

# Sign the modules(s)
%if %{?_with_modsign:1}%{!?_with_modsign:0}
# If the module signing keys are not defined, define them here.
%{!?privkey: %define privkey %{_sysconfdir}/pki/SECURE-BOOT-KEY.priv}
%{!?pubkey: %define pubkey %{_sysconfdir}/pki/SECURE-BOOT-KEY.der}
for module in $(find %{buildroot} -type f -name \*.ko);
do %{__perl} /usr/src/kernels/%{kversion}/scripts/sign-file \
sha256 %{privkey} %{pubkey} $module;
done
%endif

%clean
%{__rm} -rf %{buildroot}

%changelog
* Sat Apr 04 2020 Philip J Perry <phil@elrepo.org> - 0.0-10
- Rebuilt against RHEL 7.8 kernel
- Backported from kernel-5.3.18

* Sat Sep 07 2019 Philip J Perry <phil@elrepo.org> - 0.0-9
- Rebuilt against RHEL 7.7 kernel
- Backported from kernel-4.14.142

* Wed Nov 14 2018 Philip J Perry <phil@elrepo.org> - 0.0-8
- Rebuilt against RHEL 7.6 kernel

* Mon Jun 04 2018 Philip J Perry <phil@elrepo.org> - 0.0-7
- Backported from kernel-4.14.47 for RHEL-7.5

* Sun Jul 30 2017 Philip J Perry <phil@elrepo.org> - 0.0-6
- Backported from kernel-4.11.12 for RHEL-7.4

* Sun Nov 06 2016 Philip J Perry <phil@elrepo.org> - 0.0-5
- Backported from kernel-4.7.10 for RHEL-7.3

* Wed Nov 25 2015 Philip J Perry <phil@elrepo.org> - 0.0-4
- Backported from kernel-4.1.13 for RHEL-7.2

* Wed Mar 11 2015 Philip J Perry <phil@elrepo.org> - 0.0-3
- Updated to kernel-3.18.9 for RHEL 7.1

* Thu Mar 05 2015 Philip J Perry <phil@elrepo.org> - 0.0-2
- Rebuilt against RHEL 7.1 kernel

* Mon Jan 05 2015 Philip J Perry <phil@elrepo.org> - 0.0-1
- Initial el7 build of the kmod package.
- Backported from kernel-3.10.63
