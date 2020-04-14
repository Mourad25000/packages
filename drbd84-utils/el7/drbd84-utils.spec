%define real_name drbd-utils

Name:    drbd84-utils
Version: 9.12.2
Release: 1%{?dist}
Group:   System Environment/Kernel
License: GPLv2+
Summary: Management utilities for DRBD
URL:     http://www.drbd.org/

Source0:   http://oss.linbit.com/drbd/drbd-utils-%{version}.tar.gz

Patch1: elrepo-selinux-bug695.patch

BuildRoot:     %{_tmppath}/%{name}-%{version}-%{release}-root
BuildRequires: flex
BuildRequires: udev
BuildRequires: libxslt
BuildRequires: docbook-style-xsl
BuildRequires: po4a

Requires: udev
Requires(post):   systemd-units
Requires(preun):  systemd-units
Requires(postun): systemd-units

### Virtual provides that people may use
Provides: drbd = %{version}-%{release}
Provides: drbd84 = %{version}-%{release}

### Conflict with older Linbit packages
Conflicts: drbd < 8.4
Conflicts: drbd-utils < 8.4

### Conflict with older CentOS packages
Conflicts: drbd82 <= %{version}-%{release}
Conflicts: drbd82-utils <= %{version}-%{release}
Conflicts: drbd83 <= %{version}-%{release}
Conflicts: drbd83-utils <= %{version}-%{release}
Obsoletes: drbd84 <= %{version}-%{release}

%package sysvinit
Summary: The SysV initscript to manage the DRBD.
Group: System Environment/Daemons
Requires: %{name}%{?_isa} = %{version}-%{release}

%description
DRBD mirrors a block device over the network to another machine.
Think of it as networked raid 1. It is a building block for
setting up high availability (HA) clusters.

This packages includes the DRBD administration tools and integration
scripts for heartbeat, pacemaker, rgmanager and xen.

%description sysvinit
DRBD mirrors a block device over the network to another machine.
Think of it as networked raid 1. It is a building block for
setting up high availability (HA) clusters.

This package contains the SysV init script to manage the DRBD when
running a legacy SysV-compatible init system.

It is not required when the init system used is systemd.

%prep
%setup -n %{real_name}-%{version}
%patch1 -p1

%build
%configure \
    --with-initdir="%{_initrddir}" \
    --with-rgmanager \
    --with-initscripttype=both \
    --without-83support
%{__make} %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
%{__make} install DESTDIR="%{buildroot}"

%clean
%{__rm} -rf %{buildroot}

%post
%systemd_post drbd.service

if /usr/bin/getent group | grep -q ^haclient; then
    chgrp haclient /usr/sbin/drbdsetup
    chmod o-x,u+s /usr/sbin/drbdsetup
    chgrp haclient /usr/sbin/drbdmeta
    chmod o-x,u+s /usr/sbin/drbdmeta
fi

%preun
%systemd_preun drbd.service

%postun
%systemd_postun_with_restart drbd.service

%files
%defattr(-, root, root, 0755)
%doc ChangeLog COPYING README.md scripts/drbd.conf.example
%doc %{_mandir}/man5/drbd.conf.5*
%doc %{_mandir}/man5/drbd.conf-*
%doc %{_mandir}/man8/drbd*
%doc %{_mandir}/ja/man5/drbd.conf.5*
%doc %{_mandir}/ja/man5/drbd.conf-*
%doc %{_mandir}/ja/man8/drbd*
%doc %{_mandir}/man7/ocf_linbit_drbd.7.gz
%config %{_sysconfdir}/bash_completion.d/drbdadm
%config %{_prefix}/lib/udev/rules.d/65-drbd.rules
%config(noreplace) %{_sysconfdir}/drbd.conf
%dir %{_sysconfdir}/drbd.d/
%config(noreplace) %{_sysconfdir}/drbd.d/global_common.conf
%config %attr(644, root, root) %{_unitdir}/drbd.service
%dir %{_localstatedir}/lib/drbd/
%dir /lib/drbd/
/lib/drbd/drbd
/lib/drbd/drbdadm-84
/lib/drbd/drbdsetup-84
%{_sbindir}/drbdadm
%{_sbindir}/drbdmeta
%{_sbindir}/drbdsetup
%{_sbindir}/drbdmon
%dir %{_prefix}/lib/drbd/
%{_prefix}/lib/drbd/notify-out-of-sync.sh
%{_prefix}/lib/drbd/notify-split-brain.sh
%{_prefix}/lib/drbd/notify-emergency-reboot.sh
%{_prefix}/lib/drbd/notify-emergency-shutdown.sh
%{_prefix}/lib/drbd/notify-io-error.sh
%{_prefix}/lib/drbd/notify-pri-lost-after-sb.sh
%{_prefix}/lib/drbd/notify-pri-lost.sh
%{_prefix}/lib/drbd/notify-pri-on-incon-degr.sh
%{_prefix}/lib/drbd/notify.sh
%{_prefix}/lib/drbd/outdate-peer.sh
%{_prefix}/lib/drbd/snapshot-resync-target-lvm.sh
%{_prefix}/lib/drbd/stonith_admin-fence-peer.sh
%{_prefix}/lib/drbd/unsnapshot-resync-target-lvm.sh
%{_prefix}/lib/tmpfiles.d/drbd.conf
%{_prefix}/lib/drbd/crm-fence-peer.9.sh
%{_prefix}/lib/drbd/crm-unfence-peer.9.sh
%{_prefix}/lib/ocf/resource.d/linbit/drbd.shellfuncs.sh

### heartbeat
%{_sysconfdir}/ha.d/resource.d/drbddisk
%{_sysconfdir}/ha.d/resource.d/drbdupper

### pacemaker
%{_prefix}/lib/drbd/crm-fence-peer.sh
%{_prefix}/lib/drbd/crm-unfence-peer.sh
%{_prefix}/lib/ocf/resource.d/linbit/drbd

### rgmanager / rhcs
%{_datadir}/cluster/drbd.sh
%{_datadir}/cluster/drbd.metadata
%{_prefix}/lib/drbd/rhcs_fence

### xen
%{_sysconfdir}/xen/scripts/block-drbd

%files sysvinit
%defattr(-,root,root)
%config %{_initrddir}/drbd

%changelog
* Sat Apr 04 2020 Akemi Yagi <toracat@elrepo.org> - 9.12.2-1
- Updated to 9.12.2

* Fri Nov 02 2018 Akemi Yagi <toracat@elrepo.org> - 9.6.0-1
- Updated to 9.6.0

* Thu Apr 26 2018 Akemi Yagi <toracat@elrepo.org> - 9.3.1-1
- Updated to 9.3.1

* Fri Sep 15 2017 Akemi Yagi <toracat@elrepo.org> - 9.1.0-1
- Updated to 9.1.0

* Mon Jun 12 2017 Akemi Yagi <toracat@elrepo.org> - 9.0.0-1
- Updated to 9.0.0
- xmlto replaced with docbook-style-xsl [git PR #155]

* Sat Dec  3 2016 Akemi Yagi <toracat@elrepo.org> - 8.9.8-1
- update to version 8.9.8.
- Bug fix (elrepo bug #695)

* Wed Oct  5 2016 Hiroshi Fujishima <h-fujishima@sakura.ad.jp> - 8.9.6-1
- Update to version 8.9.6.
- BuildRequires: xmlto added by A. Yagi for building in mock.

* Mon Jan  4 2016 Hiroshi Fujishima <h-fujishima@sakura.ad.jp> - 8.9.5-1
- Update to version 8.9.5.

* Sat Aug 15 2015 Akemi Yagi <toracat@elrepo.org> - 8.9.3-1.1
- Patch drbd.ocf to the version from 8.9.3-2 (bugs #578 and #589)

* Wed Jun 24 2015 Hiroshi Fujishima <h-fujishima@sakura.ad.jp> - 8.9.3-1
- Update to version 8.9.3.

* Sat May 16 2015 Akemi Yagi <toracat@elrepo.org> - 8.9.2-2
- Added missing line %dir %{_localstatedir}/lib/drbd/ (bug#571)

* Fri Apr 10 2015 Philip J Perry <phil@elrepo.org> - 8.9.2-1
- Update to version 8.9.2.

* Sun Aug 17 2014 Jun Futagawa <jfut@integ.jp> - 8.9.1-1
- Updated to version 8.9.1

* Sun Jul 27 2014 Jun Futagawa <jfut@integ.jp> - 8.4.4-1
- Initial package for RHEL7.
