%if ! (0%{?rhel} > 5)
%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")}
%endif

%bcond_without check
%bcond_without doc

# where are all the python3 dependencies
%if 0%{?fedora} > 15
%global with_python3 1
%endif

# where are all the pypy dependencies
%if 0%{?fedora} > 15
%global with_pypy 0
%endif

Name:           ipython
Version:        3.0.0
Release:        1%{?dist}
Summary:        An enhanced interactive Python shell

Group:          Development/Libraries
# See bug #603178 for a quick overview for the choice of licenses
# most files are under BSD and just a few under Python or MIT
# There are some extensions released under GPLv2+
License:        (BSD and MIT and Python) and GPLv2+
URL:            http://ipython.org/
Source0:        https://pypi.python.org/packages/source/i/ipython/ipython-%{version}.tar.gz
# Add _jsdir to default search path
Patch0:         ipython-2.1.0-_jsdir-search-path.patch
# Port to fontawesome 4
# Sent upstream: https://github.com/ipython/ipython/pull/6084
Patch1:         ipython-2.1.0-fontawesome4.patch

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:      noarch
BuildRequires:  python-devel
%if 0%{?with_python3}
BuildRequires:  python3-devel
%endif

%if %{with doc}
%endif

%if %{with check}
# for checking/testing
BuildRequires:  Cython
BuildRequires:  python-nose
BuildRequires:  python-matplotlib
BuildRequires:  python-mock
BuildRequires:  pymongo
BuildRequires:  PyQt4
BuildRequires:  python-tornado >= 4.0
BuildRequires:  python-zmq
BuildRequires:  python-zmq-tests
# for frontend
BuildRequires:  python-pygments

%if 0%{?with_python3}
BuildRequires:  python3-Cython
BuildRequires:  python3-nose
BuildRequires:  python3-matplotlib
BuildRequires:  python3-pymongo
BuildRequires:  python3-PyQt4
BuildRequires:  python3-tornado >= 4.0
BuildRequires:  python3-zmq
BuildRequires:  python3-zmq-tests
# for frontend
BuildRequires:  python3-pygments
%endif # with_python3

# for running qt/matplotlib tests
BuildRequires:  xorg-x11-server-Xvfb
%endif # with check

# Require $current_python_interpreter-ipython
Requires:       python-ipython


%global ipython_desc_base \
IPython provides a replacement for the interactive Python interpreter with\
extra functionality.\
\
Main features:\
 * Comprehensive object introspection.\
 * Input history, persistent across sessions.\
 * Caching of output results during a session with automatically generated\
   references.\
 * Readline based name completion.\
 * Extensible system of 'magic' commands for controlling the environment and\
   performing many tasks related either to IPython or the operating system.\
 * Configuration system with easy switching between different setups (simpler\
   than changing $PYTHONSTARTUP environment variables every time).\
 * Session logging and reloading.\
 * Extensible syntax processing for special purpose situations.\
 * Access to the system shell with user-extensible alias system.\
 * Easily embeddable in other Python programs.\
 * Integrated access to the pdb debugger and the Python profiler.

%description
%{ipython_desc_base}

%package -n python-ipython
Summary:        An enhanced interactive Python shell
Requires:       python-ipython-console = %{version}-%{release}
Requires:       python-ipython-gui = %{version}-%{release}
Requires:       python-ipython-notebook = %{version}-%{release}
Provides:       ipython = %{version}-%{release}
Obsoletes:      ipython < 0.13-1

%description -n python-ipython
%{ipython_desc_base}

This package depends on all python-ipython packages but python-ipython-tests.

%package -n python-ipython-console
Summary:        An enhanced interactive Python shell for the terminal
Requires:       python-zmq

# bundled python packages
BuildRequires:  python-decorator
BuildRequires:  python-jsonschema
BuildRequires:  python-path
BuildRequires:  pexpect
BuildRequires:  python-simplegeneric
Requires:       pexpect
Requires:       python-decorator
BuildRequires:  python-mistune >= 0.3.1
Requires:       python-mistune >= 0.3.1
Requires:       python-jsonschema
Requires:       python-path
Requires:       python-simplegeneric

# for starting ipython from pkg_resources
Requires:       python-setuptools

%description -n python-ipython-console
%{ipython_desc_base}

This package provides IPython for in a terminal.

%package -n python-ipython-sphinx
Summary:        Sphinx directive to support embedded IPython code
Requires:       python-ipython-console = %{version}-%{release}
BuildRequires:  python-sphinx
Requires:       python-sphinx

%description -n python-ipython-sphinx
%{ipython_desc_base}

This package contains the ipython sphinx extension.

%package -n python-ipython-notebook
Summary:        An enhanced interactive Python notebook
Requires:       python-ipython-console = %{version}-%{release}
Requires:       python-jinja2
Requires:       python-matplotlib
BuildRequires:  python-mistune >= 0.5
Requires:       python-mistune >= 0.5
Requires:       python-tornado >= 4.0
Provides:       ipython-notebook = %{version}-%{release}
BuildRequires:  mathjax
Requires:       mathjax


#################################################
### Bundled stuff from the notebook goes here ###
#################################################
# We need to know nodejs_sitearch and lib
BuildRequires:  nodejs-packaging
BuildRequires:  web-assets-devel

BuildRequires:  fontawesome-fonts-web
Requires:       fontawesome-fonts-web
BuildRequires:  nodejs-requirejs
Requires:       nodejs-requirejs
BuildRequires:  nodejs-underscore
Requires:       nodejs-underscore
BuildRequires:  js-highlight
Requires:       js-highlight
BuildRequires:  js-marked
Requires:       js-marked

# BR of helpers for unbundling
BuildRequires:  nodejs-less
BuildRequires:  fabric


# Temporal bundling allowed in:
# https://fedorahosted.org/fpc/ticket/416
#############################################################################
# jquery temporary exception lasts until the release that jquery enters
# the repository. For now, plan on temporary exception for other libraries
# will expire one release after jquery unbundling has entered the repository.
# Lessons from the jquery unbundling may lead us to change that time frame
# as it is our proof of concept of how to unbundle.
#############################################################################
Provides:       bundled(js-backbone)
Provides:       bundled(bootstrap)
Provides:       bundled(js-bootstrap)
Provides:       bundled(bootstrap-tour)
Provides:       bundled(js-bootstrap-tour)
Provides:       bundled(codemirror)
Provides:       bundled(js-codemirror)
Provides:       bundled(js-jquery)
Provides:       bundled(js-jquery-ui)
Provides:       bundled(js-google-caja)


%description -n python-ipython-notebook
%{ipython_desc_base}

This package contains the ipython notebook.


%package -n python-ipython-tests
Summary:        Tests for %{name}
Group:          Documentation
Requires:       python-nose
Requires:       python-zmq-tests
Requires:       python-ipython-console = %{version}-%{release}
Provides:       ipython-tests = %{version}-%{release}
Obsoletes:      ipython-tests < 0.13-1
%description -n python-ipython-tests
This package contains the tests of %{name}.
You can check this way, if ipython works on your platform.


%if %{with doc}
%package -n python-ipython-doc
Summary:        Documentation for %{name}
Group:          Documentation
Provides:       ipython-doc = %{version}-%{release}
Obsoletes:      ipython-doc < 0.13-1
%description -n python-ipython-doc
This package contains the documentation of %{name}.
%endif


%package -n python-ipython-gui
Summary:        Gui applications from %{name}
Group:          Applications/Editors
Requires:       python-ipython-console = %{version}-%{release}
Requires:       PyQt4
Requires:       python-matplotlib
Requires:       python-pygments
Provides:       ipython-gui = %{version}-%{release}
Obsoletes:      ipython-gui < 0.13-1
%description -n python-ipython-gui
This package contains the gui of %{name}, which requires PyQt.



%if 0%{?with_python3}
# TODO revisit python3 packages again, once python2 restructuring is done
%package -n python3-ipython
Summary:        An enhanced interactive Python shell
Requires:       python3-ipython-console = %{version}-%{release}
Requires:       python3-ipython-gui = %{version}-%{release}
Requires:       python3-ipython-notebook = %{version}-%{release}
%description -n python3-ipython
%{ipython_desc_base}

This package depends on all python3-ipython packages but python3-ipython-tests.

%package -n python3-ipython-console
Summary:        An enhanced interactive Python shell for the terminal
Requires:       python3-zmq


# bundled python packages
BuildRequires:  python3-decorator
BuildRequires:  python3-jsonschema
BuildRequires:  python3-path
BuildRequires:  python3-pexpect
BuildRequires:  python3-simplegeneric
Requires:       python3-decorator
Requires:       python3-jsonschema
BuildRequires:  python3-mistune >= 0.3.1
Requires:       python3-mistune >= 0.3.1
Requires:       python3-path
Requires:       python3-pexpect
Requires:       python3-simplegeneric

# for starting ipython from pkg_resources
Requires:       python3-setuptools

%description -n python3-ipython-console
%{ipython_desc_base}

This package provides IPython for in a terminal.

%package -n python3-ipython-sphinx
Summary:        Sphinx directive to support embedded IPython code
Requires:       python3-ipython-console = %{version}-%{release}
BuildRequires:  python3-sphinx
Requires:       python3-sphinx

%description -n python3-ipython-sphinx
%{ipython_desc_base}

This package contains the ipython sphinx extension.


%package -n python3-ipython-notebook
Summary:        An enhanced interactive Python notebook
Requires:       python3-ipython-console = %{version}-%{release}
Requires:       python3-jinja2
Requires:       python3-matplotlib
BuildRequires:  python3-mistune >= 0.5
Requires:       python3-mistune >= 0.5
Requires:       python3-tornado >= 4.0
BuildRequires:  mathjax
Requires:       mathjax

#################################################
### Bundled stuff from the notebook goes here ###
#################################################
# We need to know nodejs_sitearch and lib
BuildRequires:  nodejs-packaging
BuildRequires:  web-assets-devel

BuildRequires:  fontawesome-fonts-web
Requires:       fontawesome-fonts-web
BuildRequires:  nodejs-requirejs
Requires:       nodejs-requirejs
BuildRequires:  nodejs-underscore
Requires:       nodejs-underscore
BuildRequires:  js-highlight
Requires:       js-highlight
BuildRequires:  js-marked
Requires:       js-marked

# Temporal bundling allowed in:
# https://fedorahosted.org/fpc/ticket/416
#############################################################################
# jquery temporary exception lasts until the release that jquery enters
# the repository. For now, plan on temporary exception for other libraries
# will expire one release after jquery unbundling has entered the repository.
# Lessons from the jquery unbundling may lead us to change that time frame
# as it is our proof of concept of how to unbundle.
#############################################################################
Provides:       bundled(js-backbone)
Provides:       bundled(bootstrap)
Provides:       bundled(js-bootstrap)
Provides:       bundled(bootstrap-tour)
Provides:       bundled(js-bootstrap-tour)
Provides:       bundled(codemirror)
Provides:       bundled(js-codemirror)
Provides:       bundled(js-jquery)
Provides:       bundled(js-jquery-ui)
Provides:       bundled(js-google-caja)


%description -n python3-ipython-notebook
%{ipython_desc_base}

This package contains the ipython notebook.


%package -n python3-ipython-tests
Summary:        Tests for %{name}
Group:          Documentation
Requires:       python3-nose
Requires:       python3-zmq-tests
Requires:       python3-ipython-console = %{version}-%{release}
%description -n python3-ipython-tests
This package contains the tests of %{name}.
You can check this way, if ipython works on your platform.

%package -n python3-ipython-doc
Summary:        Documentation for %{name}
Group:          Documentation
%description -n python3-ipython-doc
This package contains the documentation of %{name}.

%package -n python3-ipython-gui
Summary:        Gui applications from %{name}
Group:          Applications/Editors
Requires:       python3-ipython-console = %{version}-%{release}
Requires:       python3-PyQt4
Requires:       python3-matplotlib
Requires:       python3-pygments
%description -n python3-ipython-gui
This package contains the gui of %{name}, which requires PyQt.

%endif # with_python3



%prep
%setup -q

# Patches go here
%patch0 -p1 -b .jsdir
sed -i "s;_jsdir;%{_jsdir};g" \
    IPython/html/notebookapp.py
#patch1 -p1 -b .fontawesome4

# delete bundling libs
pushd IPython/external
ls -l
ls -l *

rm decorator/_decorator.py

# use decorators of numpy
rm decorators/_decorators.py

rm pexpect/_pexpect.py

rm path/_path.py

rm simplegeneric/_simplegeneric.py

# ssh modules from paramiko

popd

%define do_global_symlinking() \
pushd IPython/html/static/components \
    pushd font-awesome \
        rm -rf font \
        ln -s %{_datadir}/fonts/fontawesome font \
        for folder in css less scss; do \
            rm -rf $folder \
            ln -s %{_datadir}/font-awesome-*/${folder} \
        done \
        ls -l \
    popd \
# TODO backbone bootstrap google-caja jquery jquery-ui \
    #for folder in highlight.js requirejs underscore; do \
    for folder in requirejs underscore; do \
        rm -r ${folder} \
        ln -s %{nodejs_sitelib}/${folder} \
    done \
# Work around highlight packaging (ipython requires it in build/ subfolder...) \
# Unbundle JS stuff WITHIN build subfolder (ipython requires it there...) \
    #for folder in highlight.js; do \
    #    rm -r $folder \
    #    mkdir -p $folder \
    #    ln -s %{_jsdir}/$folder/ $folder/build \
    #done \
 \
    for folder in marked; do \
        rm -r $folder \
        mkdir -p $folder \
        ln -s %{_jsdir}/$folder/ $folder/lib \
    done \
ls -l \
ls -l * \
popd

# unbundle components
%do_global_symlinking
#asdf

#pushd IPython/html
    #fab css
#popd

%if 0%{?with_python3}
rm -rf %{py3dir}
cp -a . %{py3dir}
find %{py3dir} -name '*.py' -print0 | xargs -0 sed -i '1s|^#!python|#!%{__python3}|'
%endif # with_python3


%build
%if 0%{?with_python3}
pushd %{py3dir}
    %{__python3} setup.py build
popd
%endif # with_python3

%{__python} setup.py build


%if %{with doc}
cd docs
## TODO: fails with
##reading sources... [ 71%] api/generated/IPython.utils.io
##Sphinx error:
##'ascii' codec can't encode character u'\u0142' in position 204: ordinal not in range(128)
##make: *** [html] Error 1
#make html
mkdir -p build/html/
cd ..
%endif


%install
rm -rf %{buildroot}
%if 0%{?with_python3}
pushd %{py3dir}
    %{__python3} setup.py install -O1 --skip-build --root %{buildroot} 
popd
%endif # with_python3

%{__python} setup.py install -O1 --skip-build --root %{buildroot}

# unbundle components again...
pushd %{buildroot}%{python_sitelib}
    %do_global_symlinking
popd

%if 0%{?with_python3}
pushd %{buildroot}%{python3_sitelib}
    %do_global_symlinking
popd
%endif # with_python3

# Do we need to replace python3 with python2? Only seems to occur on rawhide, see #1123618
echo %{buildroot}%{_bindir}/{ipcluster,ipcontroller,ipengine,iptest,ipython} | xargs head -n 2
echo %{buildroot}%{_bindir}/{ipcluster,ipcontroller,ipengine,iptest,ipython} | xargs sed -i '1s|^#!python|#!%{__python}|'


%clean
rm -rf %{buildroot}


%if %{with check}
%check
%global test_groups config extensions lib testing terminal utils nbformat qt core autoreload nbconvert parallel html  js/services js/base js/notebook js/widgets js/tree
# the following group seems to block on python3.4
#kernel kernel.inprocess

# Ensure that the user's .pythonrc.py is not invoked during any tests.
export PYTHONSTARTUP=""
%if 0%{?with_python3}
pushd %{py3dir}
    mkdir -p run_tests
    pushd run_tests
    PYTHONPATH=%{buildroot}%{python3_sitelib} \
        PATH="%{buildroot}%{_bindir}:$PATH" \
        LC_ALL=en_US.UTF-8 \
        xvfb-run \
        %{buildroot}%{_bindir}/iptest3 %{test_groups} || :
    popd
popd
%endif

mkdir -p run_tests
pushd run_tests
    PYTHONPATH=%{buildroot}%{python_sitelib} \
        PATH="%{buildroot}%{_bindir}:$PATH" \
        LC_ALL=en_US.UTF-8 \
        xvfb-run \
        %{buildroot}%{_bindir}/iptest2 %{test_groups} || :
popd
%endif

%files -n python-ipython

%files -n python-ipython-console
%{_bindir}/ipython
%{_bindir}/ipython2
%{_bindir}/ipcluster
%{_bindir}/ipcluster2
%{_bindir}/ipcontroller
%{_bindir}/ipcontroller2
%{_bindir}/ipengine
%{_bindir}/ipengine2
%{_mandir}/man*/ipython.*
%{_mandir}/man*/ipengine*
%{_mandir}/man*/ipc*

%dir %{python_sitelib}/IPython
%{python_sitelib}/IPython/external
%{python_sitelib}/IPython/*.py*
%dir %{python_sitelib}/IPython/html/*
%{python_sitelib}/IPython/html/__init__.py*
%{python_sitelib}/IPython/html/nbextensions.py*
%dir %{python_sitelib}/IPython/kernel
%{python_sitelib}/IPython/kernel/*.py*
%{python_sitelib}/IPython/kernel/blocking/
%{python_sitelib}/IPython/kernel/comm/
%{python_sitelib}/IPython/kernel/inprocess/
%{python_sitelib}/IPython/kernel/ioloop/
%dir %{python_sitelib}/IPython/testing
%{python_sitelib}/IPython/testing/*.py*
%{python_sitelib}/IPython/testing/plugin
%{python_sitelib}/ipython-%{version}-py?.?.egg-info

%{python_sitelib}/IPython/config/
%{python_sitelib}/IPython/core/
%{python_sitelib}/IPython/extensions/
#%dir %{python_sitelib}/IPython/frontend/
#%{python_sitelib}/IPython/frontend/terminal/
#%{python_sitelib}/IPython/frontend/__init__.py*
#%{python_sitelib}/IPython/frontend/consoleapp.py*
%{python_sitelib}/IPython/lib/
%{python_sitelib}/IPython/nbformat/
%{python_sitelib}/IPython/nbconvert/
%{python_sitelib}/IPython/parallel/
%{python_sitelib}/IPython/terminal/
%{python_sitelib}/IPython/utils/
%{python_sitelib}/IPython/kernel/zmq/
%exclude %{python_sitelib}/IPython/kernel/zmq/gui/

# tests go into subpackage
%exclude %{python_sitelib}/IPython/*/tests/
%exclude %{python_sitelib}/IPython/*/*/tests


%files -n python-ipython-sphinx
%{python_sitelib}/IPython/sphinxext/


%files -n python-ipython-tests
%{_bindir}/iptest
%{_bindir}/iptest2
%{python_sitelib}/IPython/*/tests
%{python_sitelib}/IPython/*/*/tests


%if %{with doc}
%files -n python-ipython-doc
%doc docs/build/html
%endif


%files -n python-ipython-notebook
%{python_sitelib}/IPython/html/*
%exclude %{python_sitelib}/IPython/html/__init__.py*
%exclude %{python_sitelib}/IPython/html/nbextensions.py*


%files -n python-ipython-gui
%{python_sitelib}/IPython/kernel/resources/
%{python_sitelib}/IPython/kernel/zmq/gui
%{python_sitelib}/IPython/qt/

%if 0%{?with_python3}
%files -n python3-ipython

%files -n python3-ipython-console
%{_bindir}/ipython3
%{_bindir}/ipcluster3
%{_bindir}/ipcontroller3
%{_bindir}/ipengine3
# no man pages (yet?)
#%{_mandir}/man*/ipython3.*
#%{_mandir}/man*/ipengine3*
#%{_mandir}/man*/ipc*3*

%dir %{python3_sitelib}/IPython
%{python3_sitelib}/IPython/external
%{python3_sitelib}/IPython/__pycache__/
%{python3_sitelib}/IPython/*.py*
%dir %{python3_sitelib}/IPython/html
%{python3_sitelib}/IPython/html/__init__.py*
%{python3_sitelib}/IPython/html/nbextensions.py*
%dir %{python3_sitelib}/IPython/kernel
%{python3_sitelib}/IPython/kernel/__pycache__/
%{python3_sitelib}/IPython/kernel/*.py*
%{python3_sitelib}/IPython/kernel/blocking/
%{python3_sitelib}/IPython/kernel/comm/
%{python3_sitelib}/IPython/kernel/inprocess/
%{python3_sitelib}/IPython/kernel/ioloop/
%dir %{python3_sitelib}/IPython/testing
%{python3_sitelib}/IPython/testing/__pycache__/
%{python3_sitelib}/IPython/testing/*.py*
%{python3_sitelib}/IPython/testing/plugin
%{python3_sitelib}/ipython-%{version}-py?.?.egg-info

%{python3_sitelib}/IPython/config/
%{python3_sitelib}/IPython/core/
%{python3_sitelib}/IPython/extensions/
#%dir %{python3_sitelib}/IPython/frontend/
#%{python3_sitelib}/IPython/frontend/terminal/
#%{python3_sitelib}/IPython/frontend/__pycache__/
#%{python3_sitelib}/IPython/frontend/__init__.py*
#%{python3_sitelib}/IPython/frontend/consoleapp.py*
%{python3_sitelib}/IPython/lib/
%{python3_sitelib}/IPython/nbformat/
%{python3_sitelib}/IPython/nbconvert/
%{python3_sitelib}/IPython/parallel/
%{python3_sitelib}/IPython/terminal/
%{python3_sitelib}/IPython/utils/
%{python3_sitelib}/IPython/kernel/zmq/
%exclude %{python3_sitelib}/IPython/kernel/zmq/gui/

# tests go into subpackage
%exclude %{python3_sitelib}/IPython/*/tests/
%exclude %{python3_sitelib}/IPython/*/*/tests


%files -n python3-ipython-sphinx
%{python3_sitelib}/IPython/sphinxext/


%files -n python3-ipython-tests
%{_bindir}/iptest3
%{python3_sitelib}/IPython/*/tests
%{python3_sitelib}/IPython/*/*/tests


%if %{with doc}
##%files -n python3-ipython-doc
# ipython installs its own documentation, but we need to own the directory
##%{_datadir}/doc/python3-%{name}/
%endif


%files -n python3-ipython-notebook
%{python3_sitelib}/IPython/html/*
%exclude %{python3_sitelib}/IPython/html/__init__.py*
%exclude %{python3_sitelib}/IPython/html/nbextensions.py*


%files -n python3-ipython-gui
%{python3_sitelib}/IPython/kernel/resources/
%{python3_sitelib}/IPython/kernel/zmq/gui
%{python3_sitelib}/IPython/qt/
%endif # with_python3

%changelog
* Fri Feb 27 2015 Orion Poplawski <orion@cora.nwra.com> - 3.0.0-1
- Initial update to 3.0.0

* Thu Feb 26 2015 Orion Poplawski <orion@cora.nwra.com> - 2.4.1-1
- update to 2.4.1

* Wed Feb 25 2015 Orion Poplawski <orion@cora.nwra.com> - 2.4.0-1
- update to 2.4.0

* Fri Nov 14 2014 Orion Poplawski <orion@cora.nwra.com> - 2.3.0-1
- update to 2.3.0

* Thu Aug  7 2014 Thomas Spura <tomspur@fedoraproject.org> - 2.2.0-1
- update to 2.2.0

* Sun Jul 27 2014 Thomas Spura <tomspur@fedoraproject.org> - 2.1.0-7
- Replace python3 shebang with python2 one (#1123618)

* Sun Jul  6 2014 Thomas Spura <tomspur@fedoraproject.org> - 2.1.0-6
- port ipython to fontawesome-4 and regenerate css in build (#1006575)

* Mon Jun 23 2014 Thomas Spura <tomspur@fedoraproject.org> - 2.1.0-5
- use mathjax from _jsdir instead of cdn
- enable python3 tests

* Wed Jun 18 2014 Thomas Spura <tomspur@fedoraproject.org> - 2.1.0-4
- BR/R same fonts for python{,3}-ipython-notebook (#1006575)
- require tornado >= 3.1.0 (#1006575)

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.1.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Jun  1 2014 Thomas Spura <tomspur@fedoraproject.org> - 2.1.0-2
- package part of notebook in main package (#1103423)
- add BR python-sphinx

* Fri May 30 2014 Thomas Spura <tomspur@fedoraproject.org> - 2.1.0-1
- update to 2.1.0
- Unbundle js-marked
- Add provides for bundled exception fpc#416
- Add BR Cython
- disable python3 tests for now (possible blocking in koji)
- Add BR python-pexpect

* Fri May 30 2014 Thomas Spura <tomspur@fedoraproject.org> - 2.0.0-2
- add BR/R python-path
- fix python -> python3 sed replacement
- fix running testsuite
- fix %%files
- Unbundle js-highlight

* Fri May 30 2014 Thomas Spura <tomspur@fedoraproject.org> - 2.0.0-1
- update to 2.0.0
- bundled argparse has been dropped
- unbundle fontawesome-fonts{,-web}
- unbundle nodejs-requirejs
- unbundle nodejs-underscore
- unbundle nodejs-highlight-js

* Fri May 30 2014 Thomas Spura <tomspur@fedoraproject.org> - 1.1.0-1
- update to 1.1.0
- drop both patches (upstream)
- add python-ipython-sphinx packages
- remove %%defattr
- rename run_testsuite to check
- building docs (currently fails with an ascii error)
- unbundle jsonschema
- unbundle decorator

* Tue May 27 2014 Kalev Lember <kalevlember@gmail.com> - 0.13.2-4
- Rebuilt for https://fedoraproject.org/wiki/Changes/Python_3.4

* Mon Oct  7 2013 Thomas Spura <tomspur@fedoraproject.org> - 0.13.2-3
- install into unversioned docdir (#993848)
- R on setuptools for starting with pkg_resources (#994673)

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.13.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Apr 10 2013 Thomas Spura <tomspur@fedoraproject.org> - 0.13.2-2
- Improve package descriptions (#950530)

* Sat Apr  6 2013 Thomas Spura <tomspur@fedoraproject.org> - 0.13.2-1
- update to 0.13.2 fixes #927169, #947633
- run tests in xvfb
- reword description of ipython-tests a bit

* Thu Feb 21 2013 Thomas Spura <tomspur@fedoraproject.org> - 0.13.1-4
- More changes to build for Python 3 (mostly by Andrew McNabb, #784947)
- Update package structure of python3-ipython subpackage to match python2-ipython one's
- enable python3 build of ipython
- exclude pylab tests for now, as it is broken on python3

* Thu Feb 21 2013 Thomas Spura <tomspur@fedoraproject.org> - 0.13.1-3
- obsolete old python packages (José Matos, #882724)
- notebook and gui subpackage require matplotlib not the console anymore (#872176)

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.13.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Oct 24 2012 Thomas Spura <tomspur@fedoraproject.org> - 0.13.1-1
- update to 0.13.1 (#838031)
- run tests with en_US.UTF-8

* Thu Aug 30 2012 Thomas Spura <tomspur@fedoraproject.org> - 0.13-5
- add empty python-ipython files section
- obsolete ipython

* Wed Aug  8 2012 Thomas Spura <tomspur@fedoraproject.org> - 0.13-4
- use versioned requires/provides on ipython

* Sat Aug  4 2012 Thomas Spura <tomspur@fedoraproject.org> - 0.13-3
- use python-foo for python2-foo and provide ipython-foo

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.13-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Jun 30 2012 Thomas Spura <tomspur@fedoraproject.org> - 0.13-1
- update to new version
- R on mglob/pyparsing is obsolete
- remove patch, as it's upstream

* Fri Jan 27 2012 Thomas Spura <tomspur@fedoraproject.org> - 0.12-3
- skip no X tests
- continue with python3 support

* Sun Jan  8 2012 Thomas Spura <tomspur@fedoraproject.org> - 0.12-2
- add missing R tornado
- add _bindir to PATH to more tests pass in koji

* Mon Dec 19 2011 Thomas Spura <tomspur@fedoraproject.org> - 0.12-1
- update to new version
- bcond_without run_testsuite

* Sun Oct 23 2011 Thomas Spura <tomspur@fedoraproject.org> - 0.11-3
- add more missing R (matplotlib and pygments) (#748141)

* Tue Sep 20 2011 Michel Salim <salimma@fedoraproject.org> - 0.11-2
- make -gui subpackage depend on PyQt4, not PyQt

* Mon Jul  4 2011 Thomas Spura <tomspur@fedoraproject.org> - 0.11-1
- update to 0.11
- patches included upstream
- ipython changed bundled pretty, so redistributes it in lib now
- run testsuite
- new upstream url

* Sat Apr  9 2011 Thomas Spura <tomspur@fedoraproject.org> - 0.10.2-1
- update to new version
- patch3 is included upstream
- fixes #663823, #649281

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.10.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Nov 15 2010 Thomas Spura <tomspur@fedoraproject.org> - 0.10.1-3
- add fix for #646079 and use upstream fix for #628742

* Mon Oct 18 2010 Thomas Spura <tomspur@fedoraproject.org> - 0.10.1-2
- argparse is in python 2.7 and 3.2

* Wed Oct 13 2010 Thomas Spura <tomspur@fedoraproject.org> - 0.10.1-1
- unbundle a bit differently
- update to new version

* Tue Aug 31 2010 Thomas Spura <tomspur@fedoraproject.org> - 0.10-8
- pycolor: wrong filename -> no crash (#628742)

* Wed Jul 21 2010 David Malcolm <dmalcolm@redhat.com> - 0.10-7
- Rebuilt for https://fedoraproject.org/wiki/Features/Python_2.7/MassRebuild

* Mon Jul 19 2010 Thomas Spura <tomspur@fedoraproject.org> - 0.10-6
- add missing dependencies: pexpect and python-argparse

* Tue Jun 22 2010 Thomas Spura <tomspur@fedoraproject.org> - 0.10-5
- two more unbundled libraries in fedora

* Mon Jun 21 2010 Toshio Kuratomi <toshio@fedoraproject.org> - 0.10-4
- Update patch for import in argparse

* Fri Jun 11 2010 Thomas Spura <tomspur@fedoraproject.org> - 0.10-3
- fix license tag (#603178)
- add requires on wxpython to gui subpackage (#515570)
- start unbundling the libraries - more to come (#603937)

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
