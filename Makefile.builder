ifeq ($(PACKAGE_SET),vm)
	ifeq ($(DIST),centos7)
		RPM_SPEC_FILES := \
			python-pillow.spec
	endif
endif

NO_ARCHIVE := 1
