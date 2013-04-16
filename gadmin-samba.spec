# if I fix the string literal errors according to the wiki Problems
# page, it crashes on startup - AdamW 2009/01
%define Werror_cflags %nil

Summary:	A GTK+ administation tool for the SAMBA server
Name:		gadmin-samba
Version:	0.3.0
Release:	3
License:	GPLv3+
Group:		System/Configuration/Networking
URL:		http://www.gadmintools.org/
Source0:	http://mange.dynalias.org/linux/gadmin-samba/%{name}-%{version}.tar.gz
Source1:	%{name}.pam
Patch0:		gadmin-samba-0.3.0-fix_netlogon_script.patch
BuildRequires:	gtk+2-devel
BuildRequires:	imagemagick
BuildRequires:	desktop-file-utils
Requires:	samba-server >= 3.0
Requires:	openssl
Requires:	usermode-consoleonly
Obsoletes:	gsambad
Provides:	gsambad
Buildroot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
Gadmin-Samba is a fast and easy to use GTK+ administration tool for the
Samba server.

%prep
%setup -q
%patch0 -p1 -b .fix_netlogon

%build
%configure2_5x

perl -pi -e 's|^#define SAMBA_USER .*|#define SAMBA_USER \"root\"|g' config.h

%make

%install
rm -rf %{buildroot}

%makeinstall_std INSTALL_USER=`id -un` INSTALL_GROUP=`id -gn`

install -d %{buildroot}%{_sysconfdir}/%{name}

# pam auth
install -d %{buildroot}%{_sysconfdir}/pam.d/
install -d %{buildroot}%{_sysconfdir}/security/console.apps

install -m 644 %{SOURCE1} %{buildroot}%{_sysconfdir}/pam.d/%{name}
install -m 644 etc/security/console.apps/%{name} %{buildroot}%{_sysconfdir}/security/console.apps/%{name}

## locales
%find_lang %{name}

# Mandriva Icons
mkdir -p %{buildroot}%{_iconsdir}/hicolor/{16x16,32x32,48x48}/apps
convert -geometry 48x48 pixmaps/%{name}.png %{buildroot}%{_iconsdir}/hicolor/48x48/%{name}.png
convert -geometry 32x32 pixmaps/%{name}.png %{buildroot}%{_iconsdir}/hicolor/32x32/%{name}.png
convert -geometry 16x16 pixmaps/%{name}.png %{buildroot}%{_iconsdir}/hicolor/16x16/%{name}.png

mkdir -p %{buildroot}%{_datadir}/applications
sed -i -e 's,%{name}.png,%{name},g' desktop/%{name}.desktop
sed -i -e 's,GADMIN-SAMBA,Gadmin-Samba,g' desktop/%{name}.desktop
install -m644 desktop/%{name}.desktop %{buildroot}%{_datadir}/applications/%{name}.desktop
desktop-file-install --vendor="" \
    --remove-category="Application" \
    --add-category="Settings;Network;GTK;" \
    --dir %{buildroot}%{_datadir}/applications %{buildroot}%{_datadir}/applications/*

# Prepare usermode entry
mkdir -p %{buildroot}%{_bindir}
mv %{buildroot}%{_sbindir}/%{name} %{buildroot}%{_sbindir}/%{name}.real
ln -s %{_bindir}/consolehelper %{buildroot}%{_bindir}/%{name}

# Scripts
install -d %{buildroot}%{_bindir}
install -m 755 scripts/example.bat %{buildroot}%{_bindir}

mkdir -p %{buildroot}%{_sysconfdir}/security/console.apps
cat > %{buildroot}%{_sysconfdir}/security/console.apps/%{name} <<_EOF_
USER=root
PROGRAM=%{_sbindir}/%{name}.real
SESSION=true
FALLBACK=false
_EOF_

rm -rf %{buildroot}%{_datadir}/doc/%{name}



%clean
rm -rf %{buildroot}

%files -f %{name}.lang
%defattr(-,root,root,0755)
%doc COPYING AUTHORS ChangeLog
%config(noreplace) %{_sysconfdir}/pam.d/%{name}
%config(noreplace) %{_sysconfdir}/security/console.apps/%{name}
%dir %{_sysconfdir}/%{name}
%{_bindir}/*
%{_sbindir}/%{name}.real
%{_datadir}/pixmaps/*.png
%{_datadir}/pixmaps/%{name}/*.png
%{_datadir}/applications/*
%{_iconsdir}/hicolor/*/%{name}.png
%{_localstatedir}/lib/samba/netlogon/example.bat


%changelog
* Fri Sep 10 2010 Funda Wang <fwang@mandriva.org> 0.3.0-1mdv2011.0
+ Revision: 577109
- New version 0.3.0

* Sun Mar 14 2010 Funda Wang <fwang@mandriva.org> 0.2.9-1mdv2010.1
+ Revision: 518882
- new version 0.2.9

* Thu Jan 07 2010 Emmanuel Andry <eandry@mandriva.org> 0.2.8-1mdv2010.1
+ Revision: 487288
- New version 0.2.8

* Fri Sep 11 2009 Thierry Vignaud <tv@mandriva.org> 0.2.7-3mdv2010.0
+ Revision: 437644
- rebuild

* Sun Jan 04 2009 Adam Williamson <awilliamson@mandriva.org> 0.2.7-2mdv2009.1
+ Revision: 324171
- fix icon locations
- fix patch application for re-diffed patch
- rediff and improve name of fix_netlogon_script.patch
- install consolehelper link to /usr/bin not /usr/sbin, so it works right
- don't use ALL CAPS in menu entry
- fd.o icons
- clean description a bit
- new license policy
- disable Werror (if I try and fix it, it crashes on startup)

  + Oden Eriksson <oeriksson@mandriva.com>
    - lowercase ImageMagick

* Tue Sep 09 2008 Emmanuel Andry <eandry@mandriva.org> 0.2.7-1mdv2009.0
+ Revision: 283095
- import gadmin-samba


