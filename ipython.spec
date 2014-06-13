%if ! (0%{?fedora} > 12 || 0%{?rhel} > 5)
%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")}
%endif

Name:           ipython
Version:        0.13.2
Release:        1%{?dist}
Summary:        An enhanced interactive Python shell

Group:          Development/Libraries
License:        BSD
URL:            http://ipython.scipy.org/
Source0:        http://ipython.scipy.org/dist/%{name}-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:      noarch
BuildRequires:  python-devel
Requires:       python-foolscap
Requires:       python-twisted-core
Requires:       python-zope-interface
Requires:       python-argparse


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

%package tests
Summary:        Tests for %{name}
Group:          Documentation
Requires:       python-nose
Requires:       %{name} = %{version}-%{release}
%description tests
This package contains the tests of %{name}.
You can check this way, you can test, if ipython works on your platform.

%package doc
Summary:        Documentation for %{name}
Group:          Documentation
%description doc
This package contains the documentation of %{name}.

%package gui
Summary:        Gui applications from %{name}
Group:          Applications/Editors
Requires:       %{name} = %{version}-%{release}
%description gui
This package contains the gui of %{name}, which requires wxPython.



%prep
%setup -q


%build
%{__python} setup.py build


%install
rm -rf %{buildroot}
%{__python} setup.py install -O1 --skip-build --root %{buildroot}

# ipython installs docs automatically, but in the wrong place
mv %{buildroot}%{_datadir}/doc/%{name} \
    %{buildroot}%{_datadir}/doc/%{name}-%{version}


%clean
rm -rf %{buildroot}


%files
# -f notests.files
%defattr(-,root,root,-)
%{_bindir}/ipython
%{_bindir}/irunner
%{_bindir}/pycolor
%{_bindir}/ipcluster
%{_bindir}/ipcontroller
%{_bindir}/ipengine
%{_mandir}/man*/ipython.*
%{_mandir}/man*/ipengine*
%{_mandir}/man*/irunner*
%{_mandir}/man*/pycolor*
%{_mandir}/man*/ipc*
%dir %{python_sitelib}/IPython
%dir %{python_sitelib}/IPython/config
%{python_sitelib}/IPython/config/*.py*
%{python_sitelib}/IPython/external
%{python_sitelib}/IPython/*.py*
%dir %{python_sitelib}/IPython/frontend
%dir %{python_sitelib}/IPython/kernel
%{python_sitelib}/IPython/kernel/*.py*
%dir %{python_sitelib}/IPython/testing
%{python_sitelib}/IPython/testing/*.py*
%{python_sitelib}/IPython/testing/plugin
%{python_sitelib}/ipython-%{version}-py?.?.egg-info


%files tests
%defattr(-,root,root,-)
%{_bindir}/iptest
%{python_sitelib}/IPython/tests
%{python_sitelib}/IPython/*/tests
%{python_sitelib}/IPython/*/*/tests


%files doc
%defattr(-,root,root,-)
# ipython installs its own documentation, but we need to own the directory
%{_datadir}/doc/%{name}-%{version}

%files gui
%defattr(-,root,root,-)
%{_bindir}/ipython-wx
%{_bindir}/ipythonx
%{_mandir}/man*/ipython-wx*
%{_mandir}/man*/ipythonx*
%{python_sitelib}/IPython/gui
%{python_sitelib}/IPython/frontend/wx



%changelog
* Fri Jun 13 2014 David Cantrell <dcantrell@redhat.com> - 0.13.2-1
- Rebase to 0.13.2 to fix Unicode handling (#767404)

* Mon Apr 01 2013 David Cantrell <dcantrell@redhat.com> - 0.10-3
- ipython requires the 'argparse' module (#874133)

* Tue Apr 13 2010 Thomas Spura <tomspur@fedoraproject.org> - 0.10-2
- move docs into a subpackage
- subpackage wxPython
- subpackage tests
- use proper %%{python_site*} definitions
- make %%{files} more explicit
- add some missing R (fixes #529185, #515570)

* Tue Sep 22 2009 James Bowes <jbowes@redhat.com> - 0.10-1
- Update to 0.10

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Dec 04 2008 Ignacio Vazquez-Abrams <ivazqueznet+rpm@gmail.com> - 0.9.1-2
- Rebuild for Python 2.6

* Tue Dec 02 2008 James Bowes <jbowes@redhat.com> - 0.9.1-1
- Update to 0.9.1, specfile changes courtesy Greg Swift

* Sat Nov 29 2008 Ignacio Vazquez-Abrams <ivazqueznet+rpm@gmail.com> - 0.8.4-2
- Rebuild for Python 2.6

* Wed Jun 11 2008 James Bowes <jbowes@redhat.com> - 0.8.4-1
- Update to 0.8.4

* Fri May 30 2008 James Bowes <jbowes@redhat.com> - 0.8.3-1
- Update to 0.8.3

* Wed Dec 12 2007 James Bowes <jbowes@redhat.com> - 0.8.2-1
- Update to 0.8.2

* Sun Aug 05 2007 James Bowes <jbowes@redhat.com> - 0.8.1-2
- Remove explicit requires on python-abi.

* Sun Aug 05 2007 James Bowes <jbowes@redhat.com> - 0.8.1-1
- Update to 0.8.1

* Thu Dec 14 2006 Jason L Tibbitts III <tibbs@math.uh.edu> - 0.7.2-4
- Rebuild for new Python

* Sat Sep 16 2006 Shahms E. King <shahms@shahms.com> - 0.7.2-3
- Rebuild for FC6

* Fri Aug 11 2006 Shahms E. King <shahms@shahms.com> - 0.7.2-2
- Include, don't ghost .pyo files per new guidelines

* Mon Jun 12 2006 Shahms E. King <shahms@shahms.com> - 0.7.2-1
- Update to new upstream version

* Mon Feb 13 2006 Shahms E. King <shahms@shahms.com> - 0.7.1.fix1-2
- Rebuild for FC-5

* Mon Jan 30 2006 Shahms E. King <shahms@shahms.com> - 0.7.1.fix1-1
- New upstream 0.7.1.fix1 which fixes KeyboardInterrupt handling

* Tue Jan 24 2006 Shahms E. King <shahms@shahms.com> - 0.7.1-1
- Update to new upstream 0.7.1

* Thu Jan 12 2006 Shahms E. King <shahms@shahms.com> - 0.7-1
- Update to new upstream 0.7.0

* Mon Jun 13 2005 Shahms E. King <shahms@shahms.com> - 0.6.15-1
- Add dist tag
- Update to new upstream (0.6.15)

* Wed Apr 20 2005 Shahms E. King <shahms@shahms.com> - 0.6.13-2
- Fix devel release number

* Mon Apr 18 2005 Shahms E. King <shahms@shahms.com> - 0.6.13-1
- Update to new upstream version

* Fri Apr  1 2005 Michael Schwendt <mschwendt[AT]users.sf.net> - 0.6.12-2
- Include IPython Extensions and UserConfig directories.

* Fri Mar 25 2005 Shahms E. King <shahms@shahms.com> - 0.6.12-1
- Update to 0.6.12
- Removed unused python_sitearch define

* Tue Mar 01 2005 Shahms E. King <shahms@shahms.com> - 0.6.11-2
- Fix up %%doc file specifications
- Use offical .tar.gz, not upstream .src.rpm .tar.gz

* Tue Mar 01 2005 Shahms E. King <shahms@shahms.com> - 0.6.11-1
- Initial release to meet Fedora packaging guidelines
