%{!?python_sitelib: %define python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}

Name:           ipython
Version:        0.6.12
Release:        2
Summary:        An enhanced interactive Python shell

Group:          Development/Libraries
License:        BSD
URL:            http://ipython.scipy.org/
Source0:        http://ipython.scipy.org/dist/ipython-0.6.12.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:      noarch
BuildRequires:  python-devel
Requires:       python-abi = %(%{__python} -c "import sys ; print sys.version[:3]")

%description

IPython provides a replacement for the interactive Python interpreter with
extra functionality.

Main features:

 * Comprehensive object introspection.

 * Input history, persistent across sessions.

 * Caching of output results during a session with automatically generated
   references.

 * Readline based name completion.

 * Extensible system of 'magic' commands for controlling the environment and
   performing many tasks related either to IPython or the operating system.

 * Configuration system with easy switching between different setups (simpler
   than changing $PYTHONSTARTUP environment variables every time).

 * Session logging and reloading.

 * Extensible syntax processing for special purpose situations.

 * Access to the system shell with user-extensible alias system.

 * Easily embeddable in other Python programs.

 * Integrated access to the pdb debugger and the Python profiler. 

%prep
%setup -q


%build
CFLAGS="$RPM_OPT_FLAGS" %{__python} setup.py build


%install
rm -rf $RPM_BUILD_ROOT
%{__python} setup.py install -O1 --skip-build --root $RPM_BUILD_ROOT


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
# ipython installs its own documentation, but we need to own the directory
%{_datadir}/doc/%{name}-%{version}/
%{_mandir}/man*/*
%{_bindir}/ipython
%{_bindir}/pycolor
%dir %{python_sitelib}/IPython
%{python_sitelib}/IPython/*.py
%dir %{python_sitelib}/IPython/Extensions/
%{python_sitelib}/IPython/Extensions/*.py
%{python_sitelib}/IPython/*.pyc
%{python_sitelib}/IPython/Extensions/*.pyc
%dir %{python_sitelib}/IPython/UserConfig/
%{python_sitelib}/IPython/UserConfig/*
%ghost %{python_sitelib}/IPython/*.pyo
%ghost %{python_sitelib}/IPython/Extensions/*.pyo

%changelog
* Fri Apr  1 2005 Michael Schwendt <mschwendt[AT]users.sf.net> 0.6.12-2
- Include IPython Extensions and UserConfig directories.

* Fri Mar 25 2005 Shahms E. King <shahms@shahms.com> 0.6.12-1
- Update to 0.6.12
- Removed unused python_sitearch define

* Tue Mar 01 2005 Shahms E. King <shahms@shahms.com> 0.6.11-2
- Fix up %doc file specifications
- Use offical .tar.gz, not upstream .src.rpm .tar.gz

* Tue Mar 01 2005 Shahms E. King <shahms@shahms.com> 0.6.11-1
- Initial release to meet Fedora packaging guidelines
