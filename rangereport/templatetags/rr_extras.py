from django import template
from django.template.defaultfilters import stringfilter
from django.contrib.auth.models import User
from rangedogs.rangereport.models import Comment
import re

register = template.Library()

@register.filter()
@stringfilter
def linkusers(value):
    "Swap out usernames in [brackets] for their absolute URLs"
    return re.sub(r'\[(?P<object_id>[^]])]', "<a class=\"userlink\" href=\"%(link)s\">%(id)s</a>" % {'link' : User.objects.get(pk=object_id).get_profile().get_absolute_url(), 'id': object_id}, value)

@register.tag()
def recurse_comments(parser, token):
    """Along with the class below, this will post all comments recursively through {% recurse_comments %} tag
        Takes two arguments:
        parent_type - in quotes - the type of object to which the comments belong: "User", "Gun", "Handload", "Report", or "Comment"
        parent_id - template variable - the id of the object to which the comments belong"""
    try:
        tag_name, parent_type, parent_id = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError, "%r tag requires two arguments" % token.contents.split()[0]
    if not (parent_type[0] == parent_type[-1] and parent_type[0] in ('"', "'")):
        raise template.TemplateSyntaxError, "%r tag's first argument should be in quotes" % tag_name
    return CommentNode(parent_type[1:-1], parent_id)

class CommentNode(template.Node):
    def __init__(self, parent_type, parent_id):
        self.parent_type = parent_type
        self.parent_id = template.Variable(parent_id)

    def render(self, context):
        try:
            return self.recurse(self.parent_type, self.parent_id.resolve(context))
        except template.VariableDoesNotExist:
            return ''

    def recurse(self, parent_type, parent_id):
        to_return = ""
        if (parent_type == "User"):
            queryset = Comment.objects.filter(User_parent__pk__exact = parent_id)
        elif (parent_type == "Gun"):
            queryset = Comment.objects.filter(Gun_parent__pk__exact = parent_id)
        elif (parent_type == "Handload"):
            queryset = Comment.objects.filter(Handload_parent__pk__exact = parent_id)
        elif (parent_type == "Report"):
            queryset = Comment.objects.filter(Report_parent__pk__exact = parent_id)
        elif (parent_type == "Comment"):
            queryset = Comment.objects.filter(Comment_parent__pk__exact = parent_id)
        for comment in queryset:
            to_return += "<div class=\"comment\" id=\"" + comment.id + "\">\n"
            to_return += "<span class=\"comment_title\">" + comment.title + "</span>\n"
            to_return += "<span class=\"comment_owner\">" + comment.owner.username
            to_return += "<span class=\"comment_date\">" + comment.ctime + "</span>\n"
            to_return += "<span class=\"comment_body\">" + comment.body + "</span>\n"
            if (comment.mtime != comment.ctime):
                to_return += "<span class=\"comment_modified\">" + comment.mtime + "</span>\n"
            to_return += recurse("Comment", comment.id)
            to_return += "</div>\n\n"
        return to_return
