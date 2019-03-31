#
# Conditional build:
%bcond_with	apidocs # don't generate apidocs subpackage

Summary:	A source code converter to HTML, XHTML, RTF, TeX, LaTeX, XSL-FO, and XML
Summary(pl.UTF-8):	Konwerter kodu źródłowego do formatów HTML, XHTML, RTF, TeX, LaTeX, XSL-FO oraz XML
Name:		highlight
Version:	3.50
Release:	1
License:	GPL v3
Group:		Applications/Publishing
Source0:	http://www.andre-simon.de/zip/%{name}-%{version}.tar.bz2
# Source0-md5:	f15b50f90e095f8e79cc607382800e2e
Patch0:		%{name}-Makefile.patch
URL:		http://www.andre-simon.de/
BuildRequires:	Qt5Core-devel
BuildRequires:	Qt5Gui-devel
BuildRequires:	Qt5Widgets-devel
BuildRequires:	boost-devel
%{?with_apidocs:BuildRequires:	doxygen}
BuildRequires:	libstdc++-devel
BuildRequires:	lua53-devel
BuildRequires:	qt5-build
BuildRequires:	qt5-qmake
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
%if "%{_rpmversion}" >= "5"
BuildArch:	noarch
%endif

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

%description gui
Qt4 GUI for for highlight - a source code converter to HTML, XHTML,
RTF, TeX, LaTeX, XSL-FO, and XML.

%prep
%setup -q
%patch0 -p1

%build
%{__make} \
	CXX="%{__cxx}" \
	CXXFLAGS="%{rpmcxxflags} -std=c++11"
%{__make} gui \
	QMAKE=qmake-qt5 \
	CXX="%{__cxx}"

%{?with_apidocs:%{__make} apidocs}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%{__make} install-gui \
	DESTDIR=$RPM_BUILD_ROOT

# to avoid false `warning: Installed (but unpackaged) file(s) found:' - these files are packaged through %doc
rm -fr $RPM_BUILD_ROOT%{_docdir}/highlight

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog.adoc README.adoc README_LANGLIST.adoc README_PLUGINS.adoc README_REGEX.adoc extras
%lang(de) %doc README_DE.adoc
%attr(755,root,root) %{_bindir}/%{name}
%dir %{_datadir}/%{name}
%{_datadir}/%{name}/langDefs
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

%files gui
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/%{name}-gui
%dir %{_datadir}/%{name}/gui_files
%dir %{_datadir}/%{name}/gui_files/l10n
%lang(bg) %dir %{_datadir}/%{name}/gui_files/l10n/highlight_bg_BG.qm
%lang(cs) %dir %{_datadir}/%{name}/gui_files/l10n/highlight_cs_CZ.qm
%lang(de) %dir %{_datadir}/%{name}/gui_files/l10n/highlight_de_DE.qm
%lang(es) %dir %{_datadir}/%{name}/gui_files/l10n/highlight_es_ES.qm
%lang(fr) %dir %{_datadir}/%{name}/gui_files/l10n/highlight_fr_FR.qm
%lang(it) %dir %{_datadir}/%{name}/gui_files/l10n/highlight_it_IT.qm
%lang(zh) %dir %{_datadir}/%{name}/gui_files/l10n/highlight_zh_CN.qm
%{_datadir}/%{name}/gui_files/ext
%dir %{_datadir}/%{name}/plugins
%{_datadir}/%{name}/plugins/*.lua
%{_desktopdir}/*.desktop
%{_pixmapsdir}/*.xpm
