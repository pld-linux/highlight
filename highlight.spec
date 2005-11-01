#
%bcond_without	apidocs # don't generate apidocs subpackage
#
Summary:	A source code converter to HTML, XHTML, RTF, TeX, LaTeX, XSL-FO, and XML
Summary(pl):	Konwerter kodu ¼ród³owego do HTML, XHTML, RTF, TeX, LaTeX, XSL-FO, and XML
Name:		highlight
Version:	2.4.3
Release:	0.1
License:	GPL
Group:		Applications/Publishing
Source0:	http://www.andre-simon.de/zip/%{name}-%{version}.tar.gz
# Source0-md5:	19b0437361f84467fff11bdbeba654a0
Patch0:		%{name}-Makefile.patch
URL:		http://www.andre-simon.de/
BuildRequires:	libstdc++-devel
%{?with_apidocs:BuildRequires:	doxygen}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define _sysconfdir /etc/highlight

%description
Highlight is a universal converter from source code to HTML, XHTML,
RTF, TeX, LaTeX, XSL-FO, and XML. (X)HTML output is formatted by
Cascading Style Sheets. It supports 100 programming languages and
includes 50 highlighting color themes. It's possible to easily enhance
the parsing database. The converter includes some features to provide
a consistent layout of the input code.

%description -l pl
Highlight jest uniwersalnym konwerterem kodu ¼ród³owego do HTML,
XHTML, RTF, TeX, LaTeX, XSL-FO, and XML. Wyj¶cie (X)HTML jest
formatowane przez kaskadowe arkusze stylów (CSS). Highlight wspiera
100 jêzyków programistycznych i zawiera 50 kolorostycznych tematów
pod¶wietlania sk³adni. Umo¿liwia ³atwe ulepszanie bazy parsowania.
Konwerter zawiera pewne cechy zapewniaj±ce spójny uk³ad graficzny kodu
wej¶ciowego.

%package apidocs
Summary:	API documentation for highlight - a source code converter to HTML, XHTML, RTF, TeX, LaTeX, XSL-FO, and XML
Summary(pl):	Dokumentacja API highlight - konwertera kodu ¼ród³owego do HTML, XHTML, RTF, TeX, LaTeX, XSL-FO, and XML
Group:		Documentation

%description apidocs
API documentation for highlight - a source code converter to HTML,
XHTML, RTF, TeX, LaTeX, XSL-FO, and XML.

%description apidocs -l pl
Dokumentacja API highlight - konwertera kodu ¼ród³owego do HTML,
XHTML, RTF, TeX, LaTeX, XSL-FO, and XML.

%prep
%setup -q
%patch0 -p1

%build
%{__make} CXX="%{__cxx}" CXXFLAGS="%{rpmcxxflags}"

%{?with_apidocs:%{__make} apidocs}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

# to avoid false `warning: Installed (but unpackaged) file(s) found:' - these files are packaged through %doc
rm -fr $RPM_BUILD_ROOT/usr/share/doc/highlight

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog README README_INDENT README_REGEX TODO examples
%lang(de) %doc README_DE
%lang(es) %doc README_ES
%attr(755,root,root) %{_bindir}/*
%{_datadir}/%{name}
%{_mandir}/man1/*
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/*

%if %{with apidocs}
%files apidocs
%defattr(644,root,root,755)
%doc apidocs/html/*
%endif
