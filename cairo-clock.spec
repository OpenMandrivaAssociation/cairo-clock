%define	name	cairo-clock
%define	version	0.3.2
%define	release	%mkrel 4
%define	Summary	Cairo-rendered on-screen clock

Name:		%{name}
Version:	%{version}
Release:	%{release}
Summary:	%{Summary}
URL:		http://macslow.mine.nu/projects/cairo-clock/ 
Source0:	http://macslow.thepimp.net/projects/cairo-clock/%{name}-%{version}.tar.bz2
Source11:	%{name}-16.png
Source12:	%{name}-32.png
Source13:	%{name}-48.png
License:	GPL
Group:		Graphical desktop/GNOME
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot
Requires:	xcompmgr
BuildRequires:	gtk2-devel >= 2.2.0 pango-devel >= 1.2.0 fontconfig-devel
BuildRequires:	libtool autoconf automake >= 1.9.6 librsvg-devel

%description
Cairo-Clock is a desktop clock using cairo for rendering 
and taking advantage of the Composite extension on
newer Xorg servers.

%prep
%setup -q

%build
export LIBS="-lXext -lX11"
%configure
%make

%install
rm -rf %{buildroot}

%{makeinstall_std}

install -d %{buildroot}%{_menudir}
cat <<EOF > %{buildroot}%{_menudir}/%{name}
?package(%{name}):command="%{name}" \
	icon=%{name}.png \
	needs="x11" \
	section="More Applications/Games/Toys" \
	title="Cairo-clock"\
	longtitle="%{Summary}" \
	xdg="true"
EOF

desktop-file-install	--vendor="" \
			--remove-category="Application" \
			--add-category="X-MandrivaLinux-MoreApplications-Games-Toys" \
			--dir %{buildroot}%{_datadir}/applications %{buildroot}%{_datadir}/applications/*

install -m644 %{SOURCE11} -D %{buildroot}%{_miconsdir}/%{name}.png
install -m644 %{SOURCE12} -D %{buildroot}%{_iconsdir}/%{name}.png
install -m644 %{SOURCE13} -D %{buildroot}%{_liconsdir}/%{name}.png

cat > README.urpmi << EOF

Please note that you need composite extension enabled in X.org or Xgl.

Edit your %{_sysconfdir}/X11/xorg.conf and add this

Section "Extensions"
	Option "Composite" "Enable"
	Option "RENDER" "Enable"
EndSection

restart X and run xcompmgr -c& before to run cairo-clock.

EOF

%clean
rm -rf %{buildroot}

%post 
/sbin/ldconfig
%{update_menus}

%postun
/sbin/ldconfig
%{clean_menus}

%files
%defattr(-,root,root)
%doc AUTHORS BUGS NEWS README TODO README.urpmi
%{_bindir}/%{name}
%{_datadir}/applications/%{name}.desktop
%{_iconsdir}/%{name}.png
%{_liconsdir}/%{name}.png
%{_miconsdir}/%{name}.png
%{_mandir}/man1/%{name}.1*
%{_datadir}/pixmaps/%{name}.png
%{_datadir}/%{name}/*
%{_menudir}/%{name}

