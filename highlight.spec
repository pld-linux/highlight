#
# Conditional build:
%bcond_with	apidocs # don't generate apidocs subpackage
%bcond_without	gui # don't build Qt GUI tool

Summary:	A source code converter to HTML, XHTML, RTF, TeX, LaTeX, XSL-FO, and XML
Summary(pl.UTF-8):	Konwerter kodu źródłowego do formatów HTML, XHTML, RTF, TeX, LaTeX, XSL-FO oraz XML
Name:		highlight
Version:	4.13
Release:	1
License:	GPL v3
Group:		Applications/Publishing
Source0:	http://www.andre-simon.de/zip/%{name}-%{version}.tar.bz2
# Source0-md5:	25e6aef8901eb5cf555f36be63ce502e
Patch0:		%{name}-Makefile.patch
URL:		http://www.andre-simon.de/
BuildRequires:	boost-devel
%{?with_apidocs:BuildRequires:	doxygen}
BuildRequires:	libstdc++-devel >= 6:8
BuildRequires:	lua-devel >= 5.3
BuildRequires:	pkgconfig
BuildRequires:	rpm-build >= 4.6
BuildRequires:	rpmbuild(macros) >= 1.752
%if %{with gui}
BuildRequires:	Qt5Core-devel
BuildRequires:	Qt5Gui-devel
BuildRequires:	Qt5Widgets-devel
BuildRequires:	qt5-build
BuildRequires:	qt5-qmake
%endif
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_sysconfdir	/etc/highlight

%description
Highlight is a universal converter from source code to HTML, XHTML,
RTF, TeX, LaTeX, XSL-FO, and XML. (X)HTML output is formatted by
Cascading Style Sheets. It supports 100 programming languages and
includes 50 highlighting color themes. It's possible to easily enhance
the parsing database. The converter includes some features to provide
a consistent layout of the input code.

%description -l pl.UTF-8
Highlight jest uniwersalnym konwerterem kodu źródłowego do formatów
HTML, XHTML, RTF, TeX, LaTeX, XSL-FO, and XML. Wyjście (X)HTML jest
formatowane przez kaskadowe arkusze stylów (CSS). Highlight wspiera
100 języków programowania i zawiera 50 kolorystycznych motywów
podświetlania składni. Umożliwia łatwe ulepszanie bazy parsowania.
Konwerter zawiera pewne cechy zapewniające spójny układ graficzny kodu
wejściowego.

%package apidocs
Summary:	API documentation for highlight - a source code converter to HTML, XHTML, RTF, TeX, LaTeX, XSL-FO, and XML
Summary(pl.UTF-8):	Dokumentacja API highlight - konwertera kodu źródłowego do HTML, XHTML, RTF, TeX, LaTeX, XSL-FO oraz XML
Group:		Documentation
BuildArch:	noarch

%description apidocs
API documentation for highlight - a source code converter to HTML,
XHTML, RTF, TeX, LaTeX, XSL-FO, and XML.

%description apidocs -l pl.UTF-8
Dokumentacja API highlight - konwertera kodu źródłowego do formatu
HTML, XHTML, RTF, TeX, LaTeX, XSL-FO oraz XML.

%package gui
Summary:	GUI for highlight - a source code converter to HTML, XHTML, RTF, TeX, LaTeX, XSL-FO, and XML
Summary(pl.UTF-8):	GUI do highlight - konwertera kodu źródłowego do HTML, XHTML, RTF, TeX, LaTeX, XSL-FO oraz XML
Group:		Development/Tools
Requires:	%{name}
Requires(post,postun):	desktop-file-utils
Requires(post,postun):	gtk-update-icon-cache
Requires:	hicolor-icon-theme

%description gui
Qt4 GUI for for highlight - a source code converter to HTML, XHTML,
RTF, TeX, LaTeX, XSL-FO, and XML.

%package -n bash-completion-highlight
Summary:	Bash completion for highlight
Group:		Applications/Shells
Requires:	%{name} = %{version}-%{release}
Requires:	bash-completion >= 1:2.0
BuildArch:	noarch

%description -n bash-completion-highlight
Bash completion for highlight.

%package -n fish-completion-highlight
Summary:	fish-completion for highlight
Group:		Applications/Shells
Requires:	%{name} = %{version}-%{release}
Requires:	fish
BuildArch:	noarch

%description -n fish-completion-highlight
fish-completion for highlight.

%package -n zsh-completion-highlight
Summary:	ZSH completion for highlight
Group:		Applications/Shells
Requires:	%{name} = %{version}-%{release}
Requires:	zsh
BuildArch:	noarch

%description -n zsh-completion-highlight
ZSH completion for highlight.

%prep
%setup -q
%patch -P0 -p1

%build
%{__make} \
	CXX="%{__cxx}" \
	CXXFLAGS="%{rpmcxxflags} -std=c++17" \
	LUA_PKG_NAME="lua"
%if %{with gui}
%{__make} gui \
	QMAKE=qmake-qt5 \
	CXX="%{__cxx}"
%endif

%{?with_apidocs:%{__make} apidocs}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%if %{with gui}
%{__make} install-gui \
	DESTDIR=$RPM_BUILD_ROOT
%endif

# to avoid false `warning: Installed (but unpackaged) file(s) found:' - these files are packaged through %doc
rm -fr $RPM_BUILD_ROOT%{_docdir}/highlight

%clean
rm -rf $RPM_BUILD_ROOT

%post gui
%update_icon_cache hicolor
%update_desktop_database_post

%postun gui
%update_icon_cache hicolor
%update_desktop_database_postun

%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog.adoc README.adoc README_LANGLIST.adoc README_PLUGINS.adoc README_REGEX.adoc extras
%lang(de) %doc README_DE.adoc
%attr(755,root,root) %{_bindir}/%{name}
%dir %{_datadir}/%{name}
%{_datadir}/%{name}/langDefs
%dir %{_datadir}/%{name}/plugins
%{_datadir}/%{name}/plugins/*.lua
%{_datadir}/%{name}/themes
%{_mandir}/man1/highlight.1*
%{_mandir}/man5/filetypes.conf.5*
%dir %{_sysconfdir}
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/*

%if %{with apidocs}
%files apidocs
%defattr(644,root,root,755)
%doc apidocs/html/*
%endif

%if %{with gui}
%files gui
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/%{name}-gui
%dir %{_datadir}/%{name}/gui_files
%dir %{_datadir}/%{name}/gui_files/l10n
%lang(bg) %{_datadir}/%{name}/gui_files/l10n/highlight_bg_BG.qm
%lang(cs) %{_datadir}/%{name}/gui_files/l10n/highlight_cs_CZ.qm
%lang(de) %{_datadir}/%{name}/gui_files/l10n/highlight_de_DE.qm
%lang(es) %{_datadir}/%{name}/gui_files/l10n/highlight_es_ES.qm
%lang(fr) %{_datadir}/%{name}/gui_files/l10n/highlight_fr_FR.qm
%lang(it) %{_datadir}/%{name}/gui_files/l10n/highlight_it_IT.qm
%lang(ja) %{_datadir}/%{name}/gui_files/l10n/highlight_ja_JP.qm
%lang(zh) %{_datadir}/%{name}/gui_files/l10n/highlight_zh_CN.qm
%{_datadir}/%{name}/gui_files/ext
%{_desktopdir}/*.desktop
%{_iconsdir}/hicolor/*x*/apps/highlight.png
%endif

%files -n bash-completion-highlight
%defattr(644,root,root,755)
%{bash_compdir}/highlight

%files -n fish-completion-highlight
%defattr(644,root,root,755)
%{fish_compdir}/highlight.fish

%files -n zsh-completion-highlight
%defattr(644,root,root,755)
%{zsh_compdir}/_highlight
