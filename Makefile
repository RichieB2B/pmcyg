# Makefile for packaging 'pmcyg'
# RW Penney, April 2009

PREFIX=/usr/local
PKGNAME = pmcyg
VERSION = $(shell python -c 'import pmcyg; print pmcyg.PMCYG_VERSION')
DISTFILES = pmcyg.py example.pkgs \
	Authors.txt ChangeLog.txt LICENSE.txt \
	Makefile README.txt ToDo.txt

FQNAME = ${PKGNAME}-${VERSION}

.PHONY:
install:	pmcyg.py
	install -m 755 pmcyg.py ${PREFIX}/bin/pmcyg

.PHONY:
dist-gzip:	dist-dir
	tar -zcf ${FQNAME}.tgz ./${FQNAME}
	rm -rf ${FQNAME}

.PHONY:
dist-zip:	dist-dir
	zip -r ${FQNAME}.zip ./${FQNAME}
	rm -rf ${FQNAME}

.PHONY:
dist-dir:
	test -d ${FQNAME} || mkdir ${FQNAME}
	cp -p ${DISTFILES} ${FQNAME}/

.PHONY:
clean:
	rm -f ${FQNAME}.tgz ${FQNAME}.zip
