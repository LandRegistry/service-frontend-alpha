#! /usr/bin/env bash
set -xe

export VERSION=0.1
export INSTALL_DIR=opt/alpha/service-frontend # change this to somewhere better if you can think of one.

# build the python installable distribution of service-frontend
cd ../
python setup.py sdist
cd -

# make a virtualenv to install service-frontend healtcheck distribution package
mkdir -p build/$INSTALL_DIR
virtualenv build/$INSTALL_DIR

build/$INSTALL_DIR/bin/pip install -U pip distribute

# install service-frontend package to virtualenv
build/$INSTALL_DIR/bin/pip install ../dist/*

build/$INSTALL_DIR/bin/pip uninstall -y distribute

#copy over migration dir and manage.py script into base dir
cp -a ../migrations build/$INSTALL_DIR/
cp ../manage.py build/$INSTALL_DIR/

# copy gunicorn config for runing of app
cp gunicorn_config.py build/$INSTALL_DIR/

# reset virtualenv paths so that they match eventual install directory
cd build/$INSTALL_DIR
virtualenv-tools --update-path /$INSTALL_DIR
cd -

cd build

# build the deb package from the virtualenv containing service-frontend and all dependencies
fpm \
    -t deb -s dir -a all -n service-frontend -v $VERSION \
    --after-install ../debian/postinst \
    --after-remove ../debian/prerm \
    --url https://github.com/LandRegistry/service-frontend \
    --deb-upstart ../upstart/service-frontend \
    -x "*.pyc" \
    -x "*.pyo" \
    --description 'LR Service frontend application' \
    --license 'MIT' \
    --prefix / \
    ../../application/frontend/static=/var/www/service-frontend/ \
    .

cd -

# cleanup
mv build/*.deb .
rm -rf build
cd ../
rm -rf dist
rm -rf *.egg-info

# upload the deb to apt repo
