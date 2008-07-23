%define	name	cairo-clock
%define	version	0.3.4
%define	release	%mkrel 3
%define	Summary	Cairo-rendered on-screen clock

Name:		%{name}
Version:	%{version}
Release:	%{release}
Summary:	%{Summary}
URL:		http://macslow.mine.nu/projects/cairo-clock/ 
Source0:	http://macslow.thepimp.net/projects/cairo-clock/%{name}-%{version}.tar.gz
Source11:	%{name}-16.png
Source12:	%{name}-32.png
Source13:	%{name}-48.png
License:	GPL
Group:		Graphical desktop/GNOME
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot
BuildRequires:	gtk2-devel >= 2.2.0 pango-devel >= 1.2.0 fontconfig-devel
BuildRequires:	libtool autoconf automake >= 1.9.6 librsvg-devel
BuildRequires:	libglade2.0-devel
BuildRequires:	desktop-file-utils

%description
Cairo-Clock is a desktop clock using cairo for rendering and taking advantage
of the Composite extension on newer Xorg servers.

%prep
%setup -q

%build
export LIBS="-lXext -lX11"
%configure2_5x
%make

%install
rm -rf %{buildroot}

%{makeinstall_std}

%find_lang %{name}

desktop-file-install	--vendor="" \
			--remove-category="Application" \
			--add-category="Clock" \
			--add-category="GTK" \
			--dir %{buildroot}%{_datadir}/applications %{buildroot}%{_datadir}/applications/*

install -m644 %{SOURCE11} -D %{buildroot}%{_miconsdir}/%{name}.png
install -m644 %{SOURCE12} -D %{buildroot}%{_iconsdir}/%{name}.png
install -m644 %{SOURCE13} -D %{buildroot}%{_liconsdir}/%{name}.png

#clock doesn't display at even resolutions
perl -pi -e 's|Exec=cairo-clock|Exec=cairo-clock -w 127 -g 127||g' %buildroot/%{_datadir}/applications/cairo-clock.desktop

cat > README.urpmi << EOF

Cairo-clock requires the composite extension and a compositing manager
(compiz, beryl, xcompmgr, or properly enabled metacity) to function.

Please use Drak3D to enable these features.
EOF

%clean
rm -rf %{buildroot}

%post 
%if %mdkversion < 200900
/sbin/ldconfig
%endif
%if %mdkversion < 200900
%{update_menus}
%endif

%postun
%if %mdkversion < 200900
/sbin/ldconfig
%endif
%if %mdkversion < 200900
%{clean_menus}
%endif

%files -f %{name}.lang
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
