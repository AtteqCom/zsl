from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relation
import sqlalchemy.engine
from application import service_application

if not service_application.is_initialized():
    print "Application is not initialized."
    quit()

DeclarativeBase = declarative_base()
metadata = DeclarativeBase.metadata
metadata.bind = service_application.get_injector().get(sqlalchemy.engine.Engine)

article = Table(u'article', metadata,
    Column(u'aid', INTEGER(), primary_key=True, nullable=False),
    Column(u'aid_link', INTEGER(), ForeignKey('article.aid')),
    Column(u'mid', INTEGER(), ForeignKey('magazine.mid'), nullable=False),
    Column(u'name', VARCHAR(length=255), nullable=False),
    Column(u'perex', TEXT()),
    Column(u'body', String()),
    Column(u'update_info', VARCHAR(length=255)),
    Column(u'date_from', DATETIME(), nullable=False),
    Column(u'date_to', DATETIME(), nullable=False),
    Column(u'image_id', INTEGER(), ForeignKey('image.iid')),
    Column(u'image_description', VARCHAR(length=255)),
    Column(u'creator_id', INTEGER(), ForeignKey('user.uid')),
    Column(u'editor_id', INTEGER(), ForeignKey('user.uid')),
    Column(u'url_alias', VARCHAR(length=255)),
    Column(u'url_external', VARCHAR(length=255)),
    Column(u'map_show', Integer(), nullable=False),
    Column(u'map_lat', Float(asdecimal=True), nullable=False),
    Column(u'map_lng', Float(asdecimal=True), nullable=False),
    Column(u'map_zoom', Integer(), nullable=False),
    Column(u'active', Integer(), nullable=False),
    Column(u'ads', Integer(), nullable=False),
    Column(u'interview', Integer(), nullable=False),
    Column(u'improper', Integer(), nullable=False),
    Column(u'most_read', Integer(), nullable=False),
    Column(u'exclude_hp', Integer(), nullable=False),
    Column(u'top_news', Integer(), nullable=False),
    Column(u'top_section', Integer(), nullable=False),
    Column(u'discussion', Integer(), nullable=False),
    Column(u'pr', Integer(), nullable=False),
    Column(u'video', Integer(), nullable=False),
    Column(u'foto', Integer(), nullable=False),
    Column(u'multi', Integer(), nullable=False),
    Column(u'zoznam_title_page', Integer(), nullable=False),
    Column(u'zoznam_name', VARCHAR(length=255)),
    Column(u'special', VARCHAR(length=500)),
    Column(u'fb_verb', VARCHAR(length=255), nullable=False),
    Column(u'timestamp', TIMESTAMP(), nullable=False),
)

article_box = Table(u'article_box', metadata,
    Column(u'aid', INTEGER(), ForeignKey('article.aid'), nullable=False),
    Column(u'bid', INTEGER(), ForeignKey('box.bid'), nullable=False),
    Column(u'cid', INTEGER(), ForeignKey('container.cid'), nullable=False),
    Column(u'parameters', TEXT()),
    Column(u'order', INTEGER(), nullable=False),
    Column(u'active', Integer(), nullable=False),
    Column(u'inherit', Integer(), nullable=False),
)

article_resource = Table(u'article_resource', metadata,
    Column(u'rid', INTEGER(), ForeignKey('resource.rid'), primary_key=True, nullable=False),
    Column(u'aid', INTEGER(), ForeignKey('article.aid'), primary_key=True, nullable=False),
)

article_section = Table(u'article_section', metadata,
    Column(u'sid', INTEGER(), ForeignKey('section.sid'), primary_key=True, nullable=False),
    Column(u'aid', INTEGER(), ForeignKey('article.aid'), primary_key=True, nullable=False),
    Column(u'master', Integer(), nullable=False),
    Column(u'date', DATETIME(), nullable=False),
)

article_tag = Table(u'article_tag', metadata,
    Column(u'aid', INTEGER(), ForeignKey('article.aid'), primary_key=True, nullable=False),
    Column(u'tid', INTEGER(), ForeignKey('tag.tid'), primary_key=True, nullable=False),
)

daily_content_image = Table(u'daily_content_image', metadata,
    Column(u'dcid', INTEGER(), ForeignKey('daily_content.dcid'), primary_key=True, nullable=False),
    Column(u'iid', INTEGER(), ForeignKey('image.iid'), primary_key=True, nullable=False),
)

gallery_article = Table(u'gallery_article', metadata,
    Column(u'gid', INTEGER(), ForeignKey('gallery.gid'), primary_key=True, nullable=False),
    Column(u'aid', INTEGER(), ForeignKey('article.aid'), primary_key=True, nullable=False),
)

gallery_image = Table(u'gallery_image', metadata,
    Column(u'gid', INTEGER(), ForeignKey('gallery.gid'), primary_key=True, nullable=False),
    Column(u'iid', INTEGER(), ForeignKey('image.iid'), primary_key=True, nullable=False),
    Column(u'description', VARCHAR(length=1000)),
    Column(u'order', INTEGER(), nullable=False),
)

gallery_magazine = Table(u'gallery_magazine', metadata,
    Column(u'mid', INTEGER(), ForeignKey('magazine.mid'), primary_key=True, nullable=False),
    Column(u'gid', INTEGER(), ForeignKey('gallery.gid'), primary_key=True, nullable=False),
)

gallery_tag = Table(u'gallery_tag', metadata,
    Column(u'gid', INTEGER(), ForeignKey('gallery.gid'), primary_key=True, nullable=False),
    Column(u'tid', INTEGER(), ForeignKey('tag.tid'), primary_key=True, nullable=False),
)

gallery_video = Table(u'gallery_video', metadata,
    Column(u'gid', INTEGER(), ForeignKey('gallery.gid'), primary_key=True, nullable=False),
    Column(u'vid', INTEGER(), ForeignKey('video.vid'), primary_key=True, nullable=False),
    Column(u'description', VARCHAR(length=1000)),
    Column(u'order', INTEGER(), nullable=False),
)

image_magazine = Table(u'image_magazine', metadata,
    Column(u'mid', INTEGER(), ForeignKey('magazine.mid'), primary_key=True, nullable=False),
    Column(u'iid', INTEGER(), ForeignKey('image.iid'), primary_key=True, nullable=False),
)

image_tag = Table(u'image_tag', metadata,
    Column(u'iid', INTEGER(), ForeignKey('image.iid'), primary_key=True, nullable=False),
    Column(u'tid', INTEGER(), ForeignKey('tag.tid'), primary_key=True, nullable=False),
)

magazine_ad = Table(u'magazine_ad', metadata,
    Column(u'mid', INTEGER(), ForeignKey('magazine.mid'), nullable=False),
    Column(u'lid', INTEGER(), ForeignKey('layout.lid'), nullable=False),
    Column(u'code', VARCHAR(length=50), nullable=False),
)

menu_item = Table(u'menu_item', metadata,
    Column(u'miid', INTEGER(), primary_key=True, nullable=False),
    Column(u'parent_miid', INTEGER(), ForeignKey('menu_item.miid')),
    Column(u'meid', INTEGER(), ForeignKey('menu.meid'), nullable=False),
    Column(u'name', VARCHAR(length=255), nullable=False),
    Column(u'url', VARCHAR(length=255)),
    Column(u'url_blank', Integer(), nullable=False),
    Column(u'sid', INTEGER(), ForeignKey('section.sid')),
    Column(u'order', INTEGER(), nullable=False),
    Column(u'active', Integer(), nullable=False),
    Column(u'class', VARCHAR(length=255), nullable=False),
    Column(u'color', VARCHAR(length=7), nullable=False),
)

poll_section = Table(u'poll_section', metadata,
    Column(u'sid', INTEGER(), ForeignKey('section.sid'), primary_key=True, nullable=False),
    Column(u'pid', INTEGER(), ForeignKey('poll.pid'), primary_key=True, nullable=False),
)

scheduler_article = Table(u'scheduler_article', metadata,
    Column(u'schaid', INTEGER(), primary_key=True, nullable=False),
    Column(u'schid', INTEGER(), ForeignKey('scheduler.schid')),
    Column(u'aid', INTEGER(), ForeignKey('article.aid'), nullable=False),
    Column(u'date_from', DATETIME(), nullable=False),
    Column(u'date_to', DATETIME(), nullable=False),
    Column(u'active', Integer(), nullable=False),
    Column(u'order', INTEGER(), nullable=False),
)

section = Table(u'section', metadata,
    Column(u'sid', INTEGER(), primary_key=True, nullable=False),
    Column(u'parent_sid', INTEGER(), ForeignKey('section.sid')),
    Column(u'stid', INTEGER()),
    Column(u'mid', INTEGER(), ForeignKey('magazine.mid'), nullable=False),
    Column(u'order', INTEGER(), nullable=False),
    Column(u'name', VARCHAR(length=255), nullable=False),
    Column(u'description', VARCHAR(length=1000)),
    Column(u'templates_dir', VARCHAR(length=255)),
    Column(u'controller', VARCHAR(length=50)),
    Column(u'controller_params', VARCHAR(length=255)),
    Column(u'html_title', VARCHAR(length=255)),
    Column(u'html_description', VARCHAR(length=255)),
    Column(u'html_header', VARCHAR(length=1000)),
    Column(u'html_footer', VARCHAR(length=1000)),
    Column(u'gemius_code', VARCHAR(length=64)),
    Column(u'url_alias', VARCHAR(length=255)),
    Column(u'active', Integer(), nullable=False),
    Column(u'unfolded', Integer(), nullable=False),
    Column(u'articles', Integer(), nullable=False),
)

section_ad = Table(u'section_ad', metadata,
    Column(u'sid', INTEGER(), ForeignKey('section.sid'), nullable=False),
    Column(u'lid', INTEGER(), ForeignKey('layout.lid'), nullable=False),
    Column(u'code', VARCHAR(length=50), nullable=False),
    Column(u'recycle_pid', INTEGER(), nullable=False),
)

section_box = Table(u'section_box', metadata,
    Column(u'sid', INTEGER(), ForeignKey('section.sid'), nullable=False),
    Column(u'bid', INTEGER(), ForeignKey('box.bid'), nullable=False),
    Column(u'cid', INTEGER(), ForeignKey('container.cid'), nullable=False),
    Column(u'parameters', TEXT()),
    Column(u'order', INTEGER(), nullable=False),
    Column(u'active', Integer(), nullable=False),
    Column(u'inherit', Integer(), nullable=False),
)

section_layout = Table(u'section_layout', metadata,
    Column(u'slid', INTEGER(), primary_key=True, nullable=False),
    Column(u'sid', INTEGER(), ForeignKey('section.sid'), nullable=False),
    Column(u'lid', INTEGER(), ForeignKey('layout.lid'), nullable=False),
    Column(u'css', VARCHAR(length=255)),
    Column(u'template', VARCHAR(length=255)),
    Column(u'default', Integer(), nullable=False),
)

section_tag = Table(u'section_tag', metadata,
    Column(u'sid', INTEGER(), ForeignKey('section.sid'), primary_key=True, nullable=False),
    Column(u'tid', INTEGER(), ForeignKey('tag.tid'), primary_key=True, nullable=False),
)

user_magazine = Table(u'user_magazine', metadata,
    Column(u'mid', INTEGER(), ForeignKey('magazine.mid'), primary_key=True, nullable=False),
    Column(u'uid', INTEGER(), ForeignKey('user.uid'), primary_key=True, nullable=False),
)

user_module = Table(u'user_module', metadata,
    Column(u'mid', INTEGER(), ForeignKey('module.mid'), primary_key=True, nullable=False),
    Column(u'uid', INTEGER(), ForeignKey('user.uid'), primary_key=True, nullable=False),
    Column(u'permissions', Enum(u'RW', u'RO'), nullable=False),
)

user_section = Table(u'user_section', metadata,
    Column(u'uid', INTEGER(), ForeignKey('user.uid'), primary_key=True, nullable=False),
    Column(u'sid', INTEGER(), ForeignKey('section.sid'), primary_key=True, nullable=False),
    Column(u'permissions', Enum(u'RW', u'RO'), nullable=False),
)

video_magazine = Table(u'video_magazine', metadata,
    Column(u'mid', INTEGER(), ForeignKey('magazine.mid'), primary_key=True, nullable=False),
    Column(u'vid', INTEGER(), ForeignKey('video.vid'), primary_key=True, nullable=False),
)

video_tag = Table(u'video_tag', metadata,
    Column(u'vid', INTEGER(), ForeignKey('video.vid'), primary_key=True, nullable=False),
    Column(u'tid', INTEGER(), ForeignKey('tag.tid'), primary_key=True, nullable=False),
)

article_rating = Table(u'article_rating', metadata,
    Column(u'aid', INTEGER(), nullable=False),
    Column(u'num_votes_1', INTEGER(), nullable=False),
    Column(u'num_votes_2', INTEGER(), nullable=False),
    Column(u'num_votes_3', INTEGER(), nullable=False),
    Column(u'num_votes_4', INTEGER(), nullable=False),
    Column(u'num_votes_5', INTEGER(), nullable=False),
    Column(u'num_votes_6', INTEGER(), nullable=False),
    Column(u'num_votes_7', INTEGER(), nullable=False),
    Column(u'num_votes_8', INTEGER(), nullable=False),
    Column(u'num_votes_9', INTEGER(), nullable=False),
    Column(u'num_votes_10', INTEGER(), nullable=False),
    Column(u'num_votes_all', INTEGER(), nullable=False),
    Column(u'avg_rating', FLOAT(), nullable=False),
    Column(u'avg_rating_6hour', FLOAT(), nullable=False),
    Column(u'avg_rating_today', FLOAT(), nullable=False),
    Column(u'avg_rating_yesterday', FLOAT(), nullable=False),
    Column(u'avg_rating_week', FLOAT(), nullable=False),
    Column(u'fb_like', INTEGER(), nullable=False),
)

article_rating_log = Table(u'article_rating_log', metadata,
    Column(u'aid', INTEGER(), nullable=False),
    Column(u'ip', INTEGER()),
    Column(u'vote', INTEGER(), nullable=False),
    Column(u'timestamp', TIMESTAMP(), nullable=False),
)

daily_content_rating = Table(u'daily_content_rating', metadata,
    Column(u'dcid', INTEGER(), nullable=False),
    Column(u'num_votes_1', INTEGER(), nullable=False),
    Column(u'num_votes_2', INTEGER(), nullable=False),
    Column(u'num_votes_3', INTEGER(), nullable=False),
    Column(u'num_votes_4', INTEGER(), nullable=False),
    Column(u'num_votes_5', INTEGER(), nullable=False),
    Column(u'num_votes_6', INTEGER(), nullable=False),
    Column(u'num_votes_7', INTEGER(), nullable=False),
    Column(u'num_votes_8', INTEGER(), nullable=False),
    Column(u'num_votes_9', INTEGER(), nullable=False),
    Column(u'num_votes_10', INTEGER(), nullable=False),
    Column(u'num_votes_all', INTEGER(), nullable=False),
    Column(u'avg_rating', FLOAT(), nullable=False),
    Column(u'avg_rating_6hour', FLOAT(), nullable=False),
    Column(u'avg_rating_today', FLOAT(), nullable=False),
    Column(u'avg_rating_yesterday', FLOAT(), nullable=False),
    Column(u'avg_rating_week', FLOAT(), nullable=False),
)

daily_content_rating_log = Table(u'daily_content_rating_log', metadata,
    Column(u'dcid', INTEGER(), nullable=False),
    Column(u'ip', INTEGER()),
    Column(u'vote', INTEGER(), nullable=False),
    Column(u'timestamp', TIMESTAMP(), nullable=False),
)

gallery_rating = Table(u'gallery_rating', metadata,
    Column(u'gid', INTEGER(), nullable=False),
    Column(u'num_votes_1', INTEGER(), nullable=False),
    Column(u'num_votes_2', INTEGER(), nullable=False),
    Column(u'num_votes_3', INTEGER(), nullable=False),
    Column(u'num_votes_4', INTEGER(), nullable=False),
    Column(u'num_votes_5', INTEGER(), nullable=False),
    Column(u'num_votes_6', INTEGER(), nullable=False),
    Column(u'num_votes_7', INTEGER(), nullable=False),
    Column(u'num_votes_8', INTEGER(), nullable=False),
    Column(u'num_votes_9', INTEGER(), nullable=False),
    Column(u'num_votes_10', INTEGER(), nullable=False),
    Column(u'num_votes_all', INTEGER(), nullable=False),
    Column(u'avg_rating', FLOAT(), nullable=False),
    Column(u'avg_rating_6hour', FLOAT(), nullable=False),
    Column(u'avg_rating_today', FLOAT(), nullable=False),
    Column(u'avg_rating_yesterday', FLOAT(), nullable=False),
    Column(u'avg_rating_week', FLOAT(), nullable=False),
)

gallery_rating_log = Table(u'gallery_rating_log', metadata,
    Column(u'gid', INTEGER(), nullable=False),
    Column(u'ip', INTEGER()),
    Column(u'vote', INTEGER(), nullable=False),
    Column(u'timestamp', TIMESTAMP(), nullable=False),
)

magazine_domain = Table(u'magazine_domain', metadata,
    Column(u'mid', INTEGER(), ForeignKey('magazine.mid'), nullable=False),
    Column(u'domain', VARCHAR(length=255), nullable=False),
    Column(u'master', Integer(), nullable=False),
    Column(u'active', Integer(), nullable=False),
)

poll_log = Table(u'poll_log', metadata,
    Column(u'pid', INTEGER(), nullable=False),
    Column(u'ip', INTEGER()),
    Column(u'timestamp', TIMESTAMP(), nullable=False),
)

class Article(DeclarativeBase):
    __table__ = article


    #relation definitions
    article = relation('Article', primaryjoin='Article.aid_link==Article.aid')
    image = relation('Image', primaryjoin='Article.image_id==Image.iid')
    magazine = relation('Magazine', primaryjoin='Article.mid==Magazine.mid')
    magazines = relation('Magazine', primaryjoin='Article.aid==Article.aid_link', secondary=article, secondaryjoin='Article.mid==Magazine.mid')
    boxes = relation('Box', primaryjoin='Article.aid==article_box.c.aid', secondary=article_box, secondaryjoin='article_box.c.bid==Box.bid')
    resources = relation('Resource', primaryjoin='Article.aid==article_resource.c.aid', secondary=article_resource, secondaryjoin='article_resource.c.rid==Resource.rid')
    sections = relation('Section', primaryjoin='Article.aid==ArticleSection.aid', secondary=article_section, secondaryjoin='ArticleSection.sid==Section.sid')
    tags = relation('Tag', primaryjoin='Article.aid==article_tag.c.aid', secondary=article_tag, secondaryjoin='article_tag.c.tid==Tag.tid')
    galleries = relation('Gallery', primaryjoin='Article.aid==gallery_article.c.aid', secondary=gallery_article, secondaryjoin='gallery_article.c.gid==Gallery.gid')
    schedulers = relation('Scheduler', primaryjoin='Article.aid==SchedulerArticle.aid', secondary=scheduler_article, secondaryjoin='SchedulerArticle.schid==Scheduler.schid')


class ArticleLog(DeclarativeBase):
    __tablename__ = 'article_log'

    __table_args__ = {}

    #column definitions
    aid = Column(u'aid', INTEGER(), primary_key=True, nullable=False)
    impressions = Column(u'impressions', Integer(), nullable=False)
    interval = Column(u'interval', Integer(), primary_key=True, nullable=False)

    #relation definitions


class ArticleRelated(DeclarativeBase):
    __tablename__ = 'article_related'

    __table_args__ = {}

    #column definitions
    aid = Column(u'aid', INTEGER(), ForeignKey('article.aid'), primary_key=True, nullable=False)
    aid_related = Column(u'aid_related', INTEGER(), ForeignKey('article.aid'), primary_key=True, nullable=False)
    floating = Column(u'floating', Integer(), nullable=False)

    #relation definitions


class ArticleSection(DeclarativeBase):
    __table__ = article_section


    #relation definitions
    section = relation('Section', primaryjoin='ArticleSection.sid==Section.sid')
    article = relation('Article', primaryjoin='ArticleSection.aid==Article.aid')


class ArticleStat(DeclarativeBase):
    __tablename__ = 'article_stats'

    __table_args__ = {}

    #column definitions
    aid = Column(u'aid', INTEGER(), primary_key=True, nullable=False)
    comments = Column(u'comments', INTEGER(), nullable=False)
    date = Column(u'date', DATETIME(), nullable=False)
    impressions = Column(u'impressions', INTEGER(), nullable=False)
    impressions_3days = Column(u'impressions_3days', INTEGER(), nullable=False)
    impressions_6hours = Column(u'impressions_6hours', INTEGER(), nullable=False)
    impressions_hour = Column(u'impressions_hour', INTEGER(), nullable=False)
    impressions_month = Column(u'impressions_month', INTEGER(), nullable=False)
    impressions_today = Column(u'impressions_today', INTEGER(), nullable=False)
    impressions_week = Column(u'impressions_week', INTEGER(), nullable=False)
    master_sid = Column(u'master_sid', INTEGER(), nullable=False)
    mid = Column(u'mid', INTEGER(), nullable=False)
    name = Column(u'name', VARCHAR(length=255), nullable=False)
    rating = Column(u'rating', FLOAT(), nullable=False)

    #relation definitions


class Avizobox(DeclarativeBase):
    __tablename__ = 'avizobox'

    __table_args__ = {}

    #column definitions
    abid = Column(u'abid', INTEGER(), primary_key=True, nullable=False)
    active = Column(u'active', Integer(), nullable=False)
    name = Column(u'name', VARCHAR(length=200), nullable=False)

    #relation definitions


class AvizoboxImage(DeclarativeBase):
    __tablename__ = 'avizobox_image'

    __table_args__ = {}

    #column definitions
    abid = Column(u'abid', INTEGER(), ForeignKey('avizobox.abid'), nullable=False)
    abiid = Column(u'abiid', INTEGER(), primary_key=True, nullable=False)
    order = Column(u'order', INTEGER(), nullable=False)
    type = Column(u'type', Enum(u'image_gif', u'image_jpg', u'flash', u'banner'), nullable=False)
    url = Column(u'url', VARCHAR(length=255))

    #relation definitions
    avizobox = relation('Avizobox', primaryjoin='AvizoboxImage.abid==Avizobox.abid')


class Box(DeclarativeBase):
    __tablename__ = 'box'

    __table_args__ = {}

    #column definitions
    active = Column(u'active', Integer(), nullable=False)
    bid = Column(u'bid', INTEGER(), primary_key=True, nullable=False)
    controller = Column(u'controller', VARCHAR(length=100), nullable=False)
    controller_params = Column(u'controller_params', TEXT())
    name = Column(u'name', VARCHAR(length=100), nullable=False)

    #relation definitions
    articles = relation('Article', primaryjoin='Box.bid==article_box.c.bid', secondary=article_box, secondaryjoin='article_box.c.aid==Article.aid')
    sections = relation('Section', primaryjoin='Box.bid==section_box.c.bid', secondary=section_box, secondaryjoin='section_box.c.sid==Section.sid')


class Container(DeclarativeBase):
    __tablename__ = 'container'

    __table_args__ = {}

    #column definitions
    cid = Column(u'cid', INTEGER(), primary_key=True, nullable=False)
    code = Column(u'code', VARCHAR(length=255), nullable=False)
    name = Column(u'name', VARCHAR(length=255), nullable=False)
    order = Column(u'order', INTEGER(), nullable=False)
    slid = Column(u'slid', INTEGER(), ForeignKey('section_layout.slid'), nullable=False)
    width = Column(u'width', INTEGER())

    #relation definitions
    section_layout = relation('SectionLayout', primaryjoin='Container.slid==SectionLayout.slid')
    articles = relation('Article', primaryjoin='Container.cid==article_box.c.cid', secondary=article_box, secondaryjoin='article_box.c.aid==Article.aid')
    sections = relation('Section', primaryjoin='Container.cid==section_box.c.cid', secondary=section_box, secondaryjoin='section_box.c.sid==Section.sid')


class DailyContent(DeclarativeBase):
    __tablename__ = 'daily_content'

    __table_args__ = {}

    #column definitions
    avg_rating = Column(u'avg_rating', FLOAT(), nullable=False)
    created = Column(u'created', TIMESTAMP(), nullable=False)
    date = Column(u'date', DATE(), nullable=False)
    dcid = Column(u'dcid', INTEGER(), primary_key=True, nullable=False)
    dcmid = Column(u'dcmid', INTEGER(), ForeignKey('daily_content_module.dcmid'), nullable=False)
    description = Column(u'description', TEXT(), nullable=False)
    name = Column(u'name', VARCHAR(length=255), nullable=False)
    rid = Column(u'rid', INTEGER())
    url = Column(u'url', VARCHAR(length=255))

    #relation definitions
    daily_content_module = relation('DailyContentModule', primaryjoin='DailyContent.dcmid==DailyContentModule.dcmid')
    images = relation('Image', primaryjoin='DailyContent.dcid==daily_content_image.c.dcid', secondary=daily_content_image, secondaryjoin='daily_content_image.c.iid==Image.iid')


class DailyContentModule(DeclarativeBase):
    __tablename__ = 'daily_content_module'

    __table_args__ = {}

    #column definitions
    dcmid = Column(u'dcmid', INTEGER(), primary_key=True, nullable=False)
    image_crop_thumb_x = Column(u'image_crop_thumb_x', INTEGER(), nullable=False)
    image_crop_thumb_y = Column(u'image_crop_thumb_y', INTEGER(), nullable=False)
    image_crop_x = Column(u'image_crop_x', INTEGER(), nullable=False)
    image_crop_y = Column(u'image_crop_y', INTEGER(), nullable=False)
    image_thumb_x = Column(u'image_thumb_x', INTEGER(), nullable=False)
    image_thumb_y = Column(u'image_thumb_y', INTEGER(), nullable=False)
    image_x = Column(u'image_x', INTEGER(), nullable=False)
    image_y = Column(u'image_y', INTEGER(), nullable=False)
    mid = Column(u'mid', INTEGER(), ForeignKey('magazine.mid'), nullable=False)
    name = Column(u'name', VARCHAR(length=255), nullable=False)
    root_sid = Column(u'root_sid', INTEGER(), nullable=False)

    #relation definitions
    magazine = relation('Magazine', primaryjoin='DailyContentModule.mid==Magazine.mid')


class Export(DeclarativeBase):
    __tablename__ = 'export'

    __table_args__ = {}

    #column definitions
    active = Column(u'active', Integer(), nullable=False)
    controller_params = Column(u'controller_params', TEXT())
    description = Column(u'description', TEXT())
    eid = Column(u'eid', INTEGER(), primary_key=True, nullable=False)
    name = Column(u'name', VARCHAR(length=100), nullable=False)

    #relation definitions


class Gallery(DeclarativeBase):
    __tablename__ = 'gallery'

    __table_args__ = {}

    #column definitions
    aid = Column(u'aid', INTEGER(), ForeignKey('article.aid'))
    created = Column(u'created', TIMESTAMP(), nullable=False)
    gid = Column(u'gid', INTEGER(), primary_key=True, nullable=False)
    images_count = Column(u'images_count', SMALLINT(), nullable=False)
    name = Column(u'name', VARCHAR(length=255), nullable=False)

    #relation definitions
    article = relation('Article', primaryjoin='Gallery.aid==Article.aid')
    articles = relation('Article', primaryjoin='Gallery.gid==gallery_article.c.gid', secondary=gallery_article, secondaryjoin='gallery_article.c.aid==Article.aid')
    images = relation('Image', primaryjoin='Gallery.gid==GalleryImage.gid', secondary=gallery_image, secondaryjoin='GalleryImage.iid==Image.iid')
    magazines = relation('Magazine', primaryjoin='Gallery.gid==gallery_magazine.c.gid', secondary=gallery_magazine, secondaryjoin='gallery_magazine.c.mid==Magazine.mid')
    tags = relation('Tag', primaryjoin='Gallery.gid==gallery_tag.c.gid', secondary=gallery_tag, secondaryjoin='gallery_tag.c.tid==Tag.tid')
    videos = relation('Video', primaryjoin='Gallery.gid==GalleryVideo.gid', secondary=gallery_video, secondaryjoin='GalleryVideo.vid==Video.vid')


class GalleryImage(DeclarativeBase):
    __table__ = gallery_image


    #relation definitions
    gallery = relation('Gallery', primaryjoin='GalleryImage.gid==Gallery.gid')
    image = relation('Image', primaryjoin='GalleryImage.iid==Image.iid')


class GalleryVideo(DeclarativeBase):
    __table__ = gallery_video


    #relation definitions
    video = relation('Video', primaryjoin='GalleryVideo.vid==Video.vid')
    gallery = relation('Gallery', primaryjoin='GalleryVideo.gid==Gallery.gid')


class Grab(DeclarativeBase):
    __tablename__ = 'grab'

    __table_args__ = {}

    #column definitions
    active = Column(u'active', Integer(), nullable=False)
    grid = Column(u'grid', INTEGER(), primary_key=True, nullable=False)
    module = Column(u'module', VARCHAR(length=255), nullable=False)
    module_params = Column(u'module_params', TEXT())
    name = Column(u'name', VARCHAR(length=255), nullable=False)
    pending = Column(u'pending', Integer(), nullable=False)
    priority = Column(u'priority', SMALLINT(), nullable=False)

    #relation definitions


class GrabCron(DeclarativeBase):
    __tablename__ = 'grab_cron'

    __table_args__ = {}

    #column definitions
    day = Column(u'day', Integer())
    gcid = Column(u'gcid', INTEGER(), primary_key=True, nullable=False)
    grid = Column(u'grid', INTEGER(), ForeignKey('grab.grid'))
    hour = Column(u'hour', Integer())
    minute = Column(u'minute', Integer())
    module_params = Column(u'module_params', TEXT())
    month = Column(u'month', Integer())
    weekday = Column(u'weekday', Integer())

    #relation definitions
    grab = relation('Grab', primaryjoin='GrabCron.grid==Grab.grid')


class GrabLog(DeclarativeBase):
    __tablename__ = 'grab_log'

    __table_args__ = {}

    #column definitions
    grid = Column(u'grid', INTEGER(), ForeignKey('grab.grid'), nullable=False)
    grlid = Column(u'grlid', INTEGER(), primary_key=True, nullable=False)
    log = Column(u'log', TEXT(), nullable=False)
    timestamp = Column(u'timestamp', TIMESTAMP(), nullable=False)

    #relation definitions
    grab = relation('Grab', primaryjoin='GrabLog.grid==Grab.grid')


class Image(DeclarativeBase):
    __tablename__ = 'image'

    __table_args__ = {}

    #column definitions
    big = Column(u'big', Integer(), nullable=False)
    created = Column(u'created', TIMESTAMP(), nullable=False)
    description = Column(u'description', VARCHAR(length=1000))
    extension = Column(u'extension', VARCHAR(length=20))
    height = Column(u'height', INTEGER())
    iid = Column(u'iid', INTEGER(), primary_key=True, nullable=False)
    rid = Column(u'rid', INTEGER(), ForeignKey('resource.rid'))
    watermark = Column(u'watermark', Enum(u'none', u'light', u'dark'), nullable=False)
    width = Column(u'width', INTEGER())

    #relation definitions
    resource = relation('Resource', primaryjoin='Image.rid==Resource.rid')
    articles = relation('Article', primaryjoin='Image.iid==Article.image_id', secondary=article, secondaryjoin='Article.aid_link==Article.aid')
    daily_contents = relation('DailyContent', primaryjoin='Image.iid==daily_content_image.c.iid', secondary=daily_content_image, secondaryjoin='daily_content_image.c.dcid==DailyContent.dcid')
    galleries = relation('Gallery', primaryjoin='Image.iid==GalleryImage.iid', secondary=gallery_image, secondaryjoin='GalleryImage.gid==Gallery.gid')
    magazines = relation('Magazine', primaryjoin='Image.iid==image_magazine.c.iid', secondary=image_magazine, secondaryjoin='image_magazine.c.mid==Magazine.mid')
    tags = relation('Tag', primaryjoin='Image.iid==image_tag.c.iid', secondary=image_tag, secondaryjoin='image_tag.c.tid==Tag.tid')


class ImageSize(DeclarativeBase):
    __tablename__ = 'image_size'

    __table_args__ = {}

    #column definitions
    crop = Column(u'crop', Integer(), nullable=False)
    folder = Column(u'folder', VARCHAR(length=50), nullable=False)
    height = Column(u'height', INTEGER(), nullable=False)
    isid = Column(u'isid', INTEGER(), primary_key=True, nullable=False)
    mid = Column(u'mid', INTEGER(), ForeignKey('magazine.mid'), nullable=False)
    watermark = Column(u'watermark', Integer(), nullable=False)
    width = Column(u'width', INTEGER(), nullable=False)

    #relation definitions
    magazine = relation('Magazine', primaryjoin='ImageSize.mid==Magazine.mid')


class Interview(DeclarativeBase):
    __tablename__ = 'interview'

    __table_args__ = {}

    #column definitions
    active = Column(u'active', Integer(), nullable=False)
    aid = Column(u'aid', INTEGER(), ForeignKey('article.aid'), nullable=False)
    ivid = Column(u'ivid', INTEGER(), primary_key=True, nullable=False)
    name = Column(u'name', VARCHAR(length=255), nullable=False)

    #relation definitions
    article = relation('Article', primaryjoin='Interview.aid==Article.aid')


class InterviewQuestion(DeclarativeBase):
    __tablename__ = 'interview_question'

    __table_args__ = {}

    #column definitions
    answer = Column(u'answer', VARCHAR(length=3000), nullable=False)
    date_answer = Column(u'date_answer', DATETIME())
    date_question = Column(u'date_question', DATETIME())
    deleted = Column(u'deleted', Integer(), nullable=False)
    email = Column(u'email', VARCHAR(length=100), nullable=False)
    ip = Column(u'ip', INTEGER())
    ivid = Column(u'ivid', INTEGER(), ForeignKey('interview.ivid'), nullable=False)
    ivqid = Column(u'ivqid', INTEGER(), primary_key=True, nullable=False)
    name = Column(u'name', VARCHAR(length=100), nullable=False)
    question = Column(u'question', VARCHAR(length=3000), nullable=False)
    show = Column(u'show', Integer(), nullable=False)

    #relation definitions
    interview = relation('Interview', primaryjoin='InterviewQuestion.ivid==Interview.ivid')


class Layout(DeclarativeBase):
    __tablename__ = 'layout'

    __table_args__ = {}

    #column definitions
    code = Column(u'code', VARCHAR(length=255), nullable=False)
    lid = Column(u'lid', INTEGER(), primary_key=True, nullable=False)
    name = Column(u'name', VARCHAR(length=255), nullable=False)

    #relation definitions
    magazines = relation('Magazine', primaryjoin='Layout.lid==magazine_ad.c.lid', secondary=magazine_ad, secondaryjoin='magazine_ad.c.mid==Magazine.mid')
    sections = relation('Section', primaryjoin='Layout.lid==SectionLayout.lid', secondary=section_layout, secondaryjoin='SectionLayout.sid==Section.sid')


class Magazine(DeclarativeBase):
    __tablename__ = 'magazine'

    __table_args__ = {}

    #column definitions
    controller = Column(u'controller', VARCHAR(length=50))
    controller_params = Column(u'controller_params', VARCHAR(length=255))
    email = Column(u'email', VARCHAR(length=255))
    images_aspect = Column(u'images_aspect', FLOAT())
    images_dir = Column(u'images_dir', VARCHAR(length=255))
    images_domain = Column(u'images_domain', VARCHAR(length=255))
    images_domain_admin = Column(u'images_domain_admin', VARCHAR(length=255))
    mid = Column(u'mid', INTEGER(), primary_key=True, nullable=False)
    motto = Column(u'motto', TEXT())
    name = Column(u'name', VARCHAR(length=100), nullable=False)
    root_sid = Column(u'root_sid', INTEGER())
    templates_dir = Column(u'templates_dir', VARCHAR(length=255))
    watermark_crop = Column(u'watermark_crop', Integer(), nullable=False)
    watermark_gravity = Column(u'watermark_gravity', Enum(u'Center', u'NorthWest', u'North', u'NorthEast', u'West', u'East', u'SouthWest', u'South', u'SouthEast'), nullable=False)
    watermark_image = Column(u'watermark_image', VARCHAR(length=255))
    watermark_resize = Column(u'watermark_resize', Integer(), nullable=False)

    #relation definitions
    articles = relation('Article', primaryjoin='Magazine.mid==Article.mid', secondary=article, secondaryjoin='Article.aid_link==Article.aid')
    galleries = relation('Gallery', primaryjoin='Magazine.mid==gallery_magazine.c.mid', secondary=gallery_magazine, secondaryjoin='gallery_magazine.c.gid==Gallery.gid')
    images = relation('Image', primaryjoin='Magazine.mid==image_magazine.c.mid', secondary=image_magazine, secondaryjoin='image_magazine.c.iid==Image.iid')
    layouts = relation('Layout', primaryjoin='Magazine.mid==magazine_ad.c.mid', secondary=magazine_ad, secondaryjoin='magazine_ad.c.lid==Layout.lid')
    sections = relation('Section', primaryjoin='Magazine.mid==Section.mid', secondary=section, secondaryjoin='Section.parent_sid==Section.sid')
    users = relation('User', primaryjoin='Magazine.mid==user_magazine.c.mid', secondary=user_magazine, secondaryjoin='user_magazine.c.uid==User.uid')
    videos = relation('Video', primaryjoin='Magazine.mid==video_magazine.c.mid', secondary=video_magazine, secondaryjoin='video_magazine.c.vid==Video.vid')


class Menu(DeclarativeBase):
    __tablename__ = 'menu'

    __table_args__ = {}

    #column definitions
    active = Column(u'active', Integer(), nullable=False)
    meid = Column(u'meid', INTEGER(), primary_key=True, nullable=False)
    mid = Column(u'mid', INTEGER(), ForeignKey('magazine.mid'), nullable=False)
    name = Column(u'name', VARCHAR(length=255), nullable=False)

    #relation definitions
    magazine = relation('Magazine', primaryjoin='Menu.mid==Magazine.mid')
    menu_items = relation('MenuItem', primaryjoin='Menu.meid==MenuItem.meid', secondary=menu_item, secondaryjoin='MenuItem.parent_miid==MenuItem.miid')


class MenuItem(DeclarativeBase):
    __table__ = menu_item


    #relation definitions
    menu_item = relation('MenuItem', primaryjoin='MenuItem.parent_miid==MenuItem.miid')
    section = relation('Section', primaryjoin='MenuItem.sid==Section.sid')
    menu = relation('Menu', primaryjoin='MenuItem.meid==Menu.meid')
    menus = relation('Menu', primaryjoin='MenuItem.miid==MenuItem.parent_miid', secondary=menu_item, secondaryjoin='MenuItem.meid==Menu.meid')


class Module(DeclarativeBase):
    __tablename__ = 'module'

    __table_args__ = {}

    #column definitions
    active = Column(u'active', Integer(), nullable=False)
    controller = Column(u'controller', VARCHAR(length=50), nullable=False)
    mid = Column(u'mid', INTEGER(), primary_key=True, nullable=False)
    name = Column(u'name', VARCHAR(length=255), nullable=False)
    order = Column(u'order', INTEGER(), nullable=False)

    #relation definitions
    users = relation('User', primaryjoin='Module.mid==UserModule.mid', secondary=user_module, secondaryjoin='UserModule.uid==User.uid')


class Poll(DeclarativeBase):
    __tablename__ = 'poll'

    __table_args__ = {}

    #column definitions
    active = Column(u'active', Integer(), nullable=False)
    date_from = Column(u'date_from', DATETIME())
    date_to = Column(u'date_to', DATETIME())
    duel = Column(u'duel', Integer(), nullable=False)
    name = Column(u'name', VARCHAR(length=255), nullable=False)
    order = Column(u'order', Enum(u'random', u'text', u'votes', u'order', u'-random', u'-text', u'-votes', u'-order'), nullable=False)
    pid = Column(u'pid', INTEGER(), primary_key=True, nullable=False)
    protection = Column(u'protection', Enum(u'ip', u'cookie', u'cookie_ip'), nullable=False)
    question = Column(u'question', VARCHAR(length=1000), nullable=False)
    type = Column(u'type', Enum(u'normal', u'percent'), nullable=False)
    votes = Column(u'votes', INTEGER(), nullable=False)

    #relation definitions
    sections = relation('Section', primaryjoin='Poll.pid==poll_section.c.pid', secondary=poll_section, secondaryjoin='poll_section.c.sid==Section.sid')


class PollAnswer(DeclarativeBase):
    __tablename__ = 'poll_answer'

    __table_args__ = {}

    #column definitions
    order = Column(u'order', INTEGER(), nullable=False)
    paid = Column(u'paid', INTEGER(), primary_key=True, nullable=False)
    pid = Column(u'pid', INTEGER(), ForeignKey('poll.pid'), nullable=False)
    text = Column(u'text', VARCHAR(length=1000))
    votes = Column(u'votes', INTEGER(), nullable=False)

    #relation definitions
    poll = relation('Poll', primaryjoin='PollAnswer.pid==Poll.pid')


class Resource(DeclarativeBase):
    __tablename__ = 'resource'

    __table_args__ = {}

    #column definitions
    contact = Column(u'contact', VARCHAR(length=255))
    homepage = Column(u'homepage', VARCHAR(length=255))
    name = Column(u'name', VARCHAR(length=255), nullable=False)
    rid = Column(u'rid', INTEGER(), primary_key=True, nullable=False)
    type = Column(u'type', String(length=1), nullable=False)

    #relation definitions
    articles = relation('Article', primaryjoin='Resource.rid==article_resource.c.rid', secondary=article_resource, secondaryjoin='article_resource.c.aid==Article.aid')


class Scheduler(DeclarativeBase):
    __tablename__ = 'scheduler'

    __table_args__ = {}

    #column definitions
    active = Column(u'active', Integer())
    mid = Column(u'mid', INTEGER(), ForeignKey('magazine.mid'), nullable=False)
    name = Column(u'name', VARCHAR(length=255))
    schid = Column(u'schid', INTEGER(), primary_key=True, nullable=False)

    #relation definitions
    magazine = relation('Magazine', primaryjoin='Scheduler.mid==Magazine.mid')
    articles = relation('Article', primaryjoin='Scheduler.schid==SchedulerArticle.schid', secondary=scheduler_article, secondaryjoin='SchedulerArticle.aid==Article.aid')


class SchedulerArticle(DeclarativeBase):
    __table__ = scheduler_article


    #relation definitions
    scheduler = relation('Scheduler', primaryjoin='SchedulerArticle.schid==Scheduler.schid')
    article = relation('Article', primaryjoin='SchedulerArticle.aid==Article.aid')


class Section(DeclarativeBase):
    __table__ = section


    #relation definitions
    articles = relation('Article', primaryjoin='Section.sid==ArticleSection.sid', secondary=article_section, secondaryjoin='ArticleSection.aid==Article.aid')
    section = relation('Section', primaryjoin='Section.parent_sid==Section.sid')
    magazine = relation('Magazine', primaryjoin='Section.mid==Magazine.mid')
    menu_items = relation('MenuItem', primaryjoin='Section.sid==MenuItem.sid', secondary=menu_item, secondaryjoin='MenuItem.parent_miid==MenuItem.miid')
    polls = relation('Poll', primaryjoin='Section.sid==poll_section.c.sid', secondary=poll_section, secondaryjoin='poll_section.c.pid==Poll.pid')
    magazines = relation('Magazine', primaryjoin='Section.sid==Section.parent_sid', secondary=section, secondaryjoin='Section.mid==Magazine.mid')
    layouts = relation('Layout', primaryjoin='Section.sid==SectionLayout.sid', secondary=section_layout, secondaryjoin='SectionLayout.lid==Layout.lid')
    boxes = relation('Box', primaryjoin='Section.sid==section_box.c.sid', secondary=section_box, secondaryjoin='section_box.c.bid==Box.bid')
    tags = relation('Tag', primaryjoin='Section.sid==section_tag.c.sid', secondary=section_tag, secondaryjoin='section_tag.c.tid==Tag.tid')
    users = relation('User', primaryjoin='Section.sid==UserSection.sid', secondary=user_section, secondaryjoin='UserSection.uid==User.uid')


class SectionLayout(DeclarativeBase):
    __table__ = section_layout


    #relation definitions
    layout = relation('Layout', primaryjoin='SectionLayout.lid==Layout.lid')
    section = relation('Section', primaryjoin='SectionLayout.sid==Section.sid')


class SectionRelated(DeclarativeBase):
    __tablename__ = 'section_related'

    __table_args__ = {}

    #column definitions
    sid = Column(u'sid', INTEGER(), ForeignKey('section.sid'), primary_key=True, nullable=False)
    sid_related = Column(u'sid_related', INTEGER(), ForeignKey('section.sid'), primary_key=True, nullable=False)

    #relation definitions


class SectionType(DeclarativeBase):
    __tablename__ = 'section_type'

    __table_args__ = {}

    #column definitions
    code = Column(u'code', VARCHAR(length=255), nullable=False)
    name = Column(u'name', VARCHAR(length=255), nullable=False)
    stid = Column(u'stid', INTEGER(), primary_key=True, nullable=False)

    #relation definitions


class Sport(DeclarativeBase):
    __tablename__ = 'sport'

    __table_args__ = {}

    #column definitions
    id = Column(u'id', INTEGER(), primary_key=True, nullable=False)
    name = Column(u'name', VARCHAR(length=255), nullable=False)

    #relation definitions


class State(DeclarativeBase):
    __tablename__ = 'state'

    __table_args__ = {}

    #column definitions
    id = Column(u'id', INTEGER(), primary_key=True, nullable=False)
    name_en = Column(u'name_en', VARCHAR(length=64), nullable=False)
    name_sk = Column(u'name_sk', VARCHAR(length=64), nullable=False)

    #relation definitions


class Tag(DeclarativeBase):
    __tablename__ = 'tag'

    __table_args__ = {}

    #column definitions
    description = Column(u'description', VARCHAR(length=255), nullable=False)
    name = Column(u'name', VARCHAR(length=255), nullable=False)
    ref_articles = Column(u'ref_articles', INTEGER(), nullable=False)
    tcid = Column(u'tcid', INTEGER(), ForeignKey('tag_category.tcid'))
    tid = Column(u'tid', INTEGER(), primary_key=True, nullable=False)

    #relation definitions
    tag_category = relation('TagCategory', primaryjoin='Tag.tcid==TagCategory.tcid')
    articles = relation('Article', primaryjoin='Tag.tid==article_tag.c.tid', secondary=article_tag, secondaryjoin='article_tag.c.aid==Article.aid')
    galleries = relation('Gallery', primaryjoin='Tag.tid==gallery_tag.c.tid', secondary=gallery_tag, secondaryjoin='gallery_tag.c.gid==Gallery.gid')
    images = relation('Image', primaryjoin='Tag.tid==image_tag.c.tid', secondary=image_tag, secondaryjoin='image_tag.c.iid==Image.iid')
    sections = relation('Section', primaryjoin='Tag.tid==section_tag.c.tid', secondary=section_tag, secondaryjoin='section_tag.c.sid==Section.sid')
    videos = relation('Video', primaryjoin='Tag.tid==video_tag.c.tid', secondary=video_tag, secondaryjoin='video_tag.c.vid==Video.vid')


class TagCategory(DeclarativeBase):
    __tablename__ = 'tag_category'

    __table_args__ = {}

    #column definitions
    name = Column(u'name', VARCHAR(length=255), nullable=False)
    tcid = Column(u'tcid', INTEGER(), primary_key=True, nullable=False)

    #relation definitions


class User(DeclarativeBase):
    __tablename__ = 'user'

    __table_args__ = {}

    #column definitions
    active = Column(u'active', Integer(), nullable=False)
    deleted = Column(u'deleted', Integer(), nullable=False)
    email = Column(u'email', VARCHAR(length=50))
    login = Column(u'login', VARCHAR(length=50), nullable=False)
    password = Column(u'password', VARCHAR(length=32))
    superadmin = Column(u'superadmin', Integer(), nullable=False)
    uid = Column(u'uid', INTEGER(), primary_key=True, nullable=False)

    #relation definitions
    articles = relation('Article', primaryjoin='User.uid==Article.creator_id', secondary=article, secondaryjoin='Article.aid_link==Article.aid')
    magazines = relation('Magazine', primaryjoin='User.uid==user_magazine.c.uid', secondary=user_magazine, secondaryjoin='user_magazine.c.mid==Magazine.mid')
    modules = relation('Module', primaryjoin='User.uid==UserModule.uid', secondary=user_module, secondaryjoin='UserModule.mid==Module.mid')
    sections = relation('Section', primaryjoin='User.uid==UserSection.uid', secondary=user_section, secondaryjoin='UserSection.sid==Section.sid')


class UserModule(DeclarativeBase):
    __table__ = user_module


    #relation definitions
    user = relation('User', primaryjoin='UserModule.uid==User.uid')
    module = relation('Module', primaryjoin='UserModule.mid==Module.mid')


class UserSection(DeclarativeBase):
    __table__ = user_section


    #relation definitions
    user = relation('User', primaryjoin='UserSection.uid==User.uid')
    section = relation('Section', primaryjoin='UserSection.sid==Section.sid')


class Video(DeclarativeBase):
    __tablename__ = 'video'

    __table_args__ = {}

    #column definitions
    created = Column(u'created', TIMESTAMP(), nullable=False)
    description = Column(u'description', VARCHAR(length=1000))
    external_code = Column(u'external_code', TEXT())
    height = Column(u'height', INTEGER())
    name = Column(u'name', VARCHAR(length=255), nullable=False)
    rid = Column(u'rid', INTEGER(), ForeignKey('resource.rid'))
    vid = Column(u'vid', INTEGER(), primary_key=True, nullable=False)
    width = Column(u'width', INTEGER())

    #relation definitions
    resource = relation('Resource', primaryjoin='Video.rid==Resource.rid')
    galleries = relation('Gallery', primaryjoin='Video.vid==GalleryVideo.vid', secondary=gallery_video, secondaryjoin='GalleryVideo.gid==Gallery.gid')
    magazines = relation('Magazine', primaryjoin='Video.vid==video_magazine.c.vid', secondary=video_magazine, secondaryjoin='video_magazine.c.mid==Magazine.mid')
    tags = relation('Tag', primaryjoin='Video.vid==video_tag.c.vid', secondary=video_tag, secondaryjoin='video_tag.c.tid==Tag.tid')


