#%global commit0 bdbb4da0979fbdc079cf98410cdb31cf799e83b3
#%global shortcommit0 %(c=%{commit0}; echo ${c:0:7})

Name:           nvme-cli
Version:        1.6
Release:        4%{?dist}
Summary:        NVMe management command line interface

License:        GPLv2+
URL:            https://github.com/linux-nvme/nvme-cli
#Source0:        https://github.com/linux-nvme/%{name}/archive/%{commit0}.tar.gz
Source0:        https://github.com/linux-nvme/%{name}/archive/v%{version}.tar.gz

Patch0:         0001-nvme-discover-Retry-discovery-log-if-the-generation-.patch
Patch1:         0002-nvme-ioctl-retrieve-log-pages-in-4k-chunks.patch
Patch2:         0003-nvme-discover-Re-check-generation-counter-after-log-.patch
Patch3:         0004-nvme-cli-report-subsystem-reset-not-supported-by-con.patch
Patch4:         0005-nvme-list-fix-nvme-list-output-if-identify-failed-on.patch
Patch5:         0006-nvme-rem-first-perror-on-subsystem-reset-failure-.patch

BuildRequires:	libuuid-devel
BuildRequires:	gcc

%description
nvme-cli provides NVM-Express user space tooling for Linux.

%prep
#%setup -qn %{name}-%{commit0}
%setup
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1

%build
make PREFIX=/usr CFLAGS="%{optflags} -std=c99" LDFLAGS="%{__global_ldflags}" %{?_smp_mflags}


%install
%make_install PREFIX=/usr


%files
%license LICENSE
%doc README.md
%{_sbindir}/nvme
%{_mandir}/man1/nvme*.gz
%{_datadir}/bash_completion.d/nvme

%clean
rm -rf $RPM_BUILD_ROOT

%post
if [ $1 = 1 ]; then # 1 : This package is being installed for the first time
	if [ ! -f /etc/nvme/hostnqn ]; then
		install -D /dev/null /etc/nvme/hostnqn
		echo $(nvme gen-hostnqn) > /etc/nvme/hostnqn
		chmod 644 /etc/nvme/hostnqn
        fi
        if [ ! -f /etc/nvme/hostid ]; then
                uuidgen > /etc/nvme/hostid
        fi
fi

%preun
if [ -d /etc/nvme ]; then
	rm -f /etc/nvme/hostnqn
	rm -f /etc/nvme/hostid
	if [ ! -n "`ls -A /etc/nvme`" ]; then
		rm -rf /etc/nvme
	fi
fi

%changelog
* Tue Oct 16 2018 dmilburn@redhat.com - 1.6-2
- Pull in upstream fixes

* Tue Jul 24 2018 luto@kernel.org - 1.6-1
- Update to 1.6

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.4-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.4-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Nov 22 2017 luto@kernel.org - 1.4-1
- Update to 1.4

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Mon May 22 2017 luto@kernel.org - 1.3-1
- Update to 1.3

* Wed Apr 19 2017 luto@kernel.org - 1.2-2
- Update to 1.2
- 1.2-1 never existed

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Wed Feb 01 2017 luto@kernel.org - 1.1-1
- Update to 1.1

* Sun Nov 20 2016 luto@kernel.org - 1.0-1
- Update to 1.0

* Mon Oct 31 2016 luto@kernel.org - 0.9-1
- Update to 0.9

* Thu Jun 30 2016 luto@kernel.org - 0.8-1
- Update to 0.8

* Tue May 31 2016 luto@kernel.org - 0.7-1
- Update to 0.7

* Fri Mar 18 2016 luto@kernel.org - 0.5-1
- Update to 0.5

* Sun Mar 06 2016 luto@kernel.org - 0.4-1
- Update to 0.4

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.2-3.20160112gitbdbb4da
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jan 20 2016 luto@kernel.org - 0.2-2.20160112gitbdbb4da
- Update to new upstream commit, fixing #49.  "nvme list" now works.

* Wed Jan 13 2016 luto@kernel.org - 0.2-1.20160112gitde3e0f1
- Initial import.
