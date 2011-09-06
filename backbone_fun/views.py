import re

from docutils.core import publish_parts
from pyramid.httpexceptions import HTTPFound, HTTPNotFound
from pyramid.url import route_url

from pyramid.response import Response
from pyramid.view import view_config

from backbone_fun.models import DBSession
from backbone_fun.models import Page

# regular expression used to find WikiWords
wikiwords = re.compile(r"\b([A-Z]\w+[A-Z]+\w+)")

@view_config(route_name='post', request_method='GET', renderer='json')
def show_post_view(request):
    return request.matchdict

@view_config(route_name='post', request_method='DELETE', renderer='json')
def delete_post_view(request):
    return request.matchdict

#@view_config(route_name='tweet_api', renderer='json')

def view_wiki(request):
    return HTTPFound(location = request.route_url('view_page', 
                                          pagename='FrontPage'))
def view_pages(request):
    session = DBSession()
    pages = session.query(Page).all()
    return dict(pages=pages)
      
def view_page(request):
    pagename = request.matchdict['pagename']
    session = DBSession()
    page = session.query(Page).filter_by(name=pagename).first()
    if page is None:
        return HTTPNotFound('No such page')

    def check(match):
        word = match.group(1)
        exists = session.query(Page).filter_by(name=word).all()
        if exists:
            view_url = route_url('view_page', request, pagename=word)
            return '<a href="%s">%s</a>' % (view_url, word)
        else:
            add_url = route_url('add_page', request, pagename=word)
            return '<a href="%s">%s</a>' % (add_url, word)

    content = publish_parts(page.data, writer_name='html')['html_body']
    content = wikiwords.sub(check, content)
    edit_url = route_url('edit_page', request, pagename=pagename)
    return dict(page=page, content=content, edit_url=edit_url)

def add_page(request):
    name = request.matchdict['pagename']
    if 'form.submitted' in request.params:
        session = DBSession()
        body = request.params['body']
        page = Page(name, body)
        session.add(page)
        return HTTPFound(location = route_url('view_page', request,
                                              pagename=name))
    save_url = route_url('add_page', request, pagename=name)
    page = Page('', '')
    return dict(page=page, save_url=save_url)

def edit_page(request):
    name = request.matchdict['pagename']
    session = DBSession()
    page = session.query(Page).filter_by(name=name).one()
    if 'form.submitted' in request.params:
        page.data = request.params['body']
        session.add(page)
        return HTTPFound(location = route_url('view_page', request,
                                              pagename=name))
    return dict(
        page=page,
        save_url = route_url('edit_page', request, pagename=name),
        )
    
