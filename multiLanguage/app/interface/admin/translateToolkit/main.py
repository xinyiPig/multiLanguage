from translate.convert import po2xliff
import six
def args(src, tgt, **kwargs):
    arg_list = []
    arg_list.extend([u'--errorlevel=traceback', src, tgt])
    for flag, value in six.iteritems(kwargs):
        value = six.text_type(value)
        if len(flag) == 1:
            arg_list.append(u'-%s' % flag)
        else:
            arg_list.append(u'--%s' % flag)
        if value is not None:
            arg_list.append(value)
    return arg_list

# po2xliff.main(args(u'./test.po',u'./test.xliff'))