import os

import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
from tornado.options import define, options

import os.path
import json

import constants
import semantics as sem
import morphology as mr

define("port", default=8888, help="run on the given port", type=int)


# define("host", default="0.0.0.0") ##localhost now

class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (constants.root_link, RootHandler),
            (constants.api_link, APIHandler),
            (constants.associations_link, AssociationsHandler),
            (constants.vectors_link, VectorsHandler),
            (constants.same_stem_russian_link, SameStemRussianHandler),
            (constants.part_of_speech_link, PartSpeechHandler),
            (constants.similarity_link, SimilarityHandler),
            (constants.make_a_move_link, MakeMoveHandler)
        ]
        settings = dict(
            template_path=os.path.join(os.path.dirname(__file__), "templates"),
            xsrf_cookies=True,
            # TODO
            cookie_secret="__TODO:_GENERATE_YOUR_OWN_RANDOM_VALUE_HERE__",
            login_url="/auth/login",
            static_path=os.path.join(os.path.dirname(__file__), "static"),
        )
        tornado.web.Application.__init__(self, handlers, **settings)


class BaseHandler(tornado.web.RequestHandler):
    pass


class RootHandler(BaseHandler):
    async def get(self):
        self.render(constants.index_page, github_link=constants.github_link, api_link=constants.api_link,
                    contact_email=constants.contact_email)


class APIHandler(BaseHandler):
    async def get(self):
        self.render(constants.api_page, github_link=constants.github_link, api_link=constants.api_link,
                    contact_email=constants.contact_email)


class AssociationsHandler(BaseHandler):
    async def get(self, slug=None):
        try:
            key_dict = json.loads(slug)
            self.render(constants.empty_page,
                        response=json.dumps(sem.get_associations(key_dict['word'], model, key_dict['count']),
                                            separators=(',', ':'),
                                            sort_keys=True, indent=4, ensure_ascii=False).encode('utf-8'))
        except KeyError:
            self.render(constants.key_error_page)
        except ValueError:
            self.render(constants.value_error_page)


class VectorsHandler(BaseHandler):
    async def get(self, slug=None):
        try:
            key_dict = json.loads(slug)
            self.render(constants.empty_page,
                        response=json.dumps([i.tolist() for i in sem.get_vectors(key_dict['words'], model)],
                                            separators=(',', ':'),
                                            sort_keys=True, indent=4, ensure_ascii=False).encode('utf-8'))
        except KeyError:
            self.render(constants.key_error_page)
        except ValueError:
            self.render(constants.value_error_page)


class SimilarityHandler(BaseHandler):
    async def get(self, slug=None):
        try:
            key_dict = json.loads(slug)
            self.render(constants.empty_page,
                        response=json.dumps(sem.get_similarity(key_dict['word1'], key_dict['word2'], model),
                                            separators=(',', ':'),
                                            sort_keys=True, indent=4, ensure_ascii=False).encode('utf-8'))
        except KeyError:
            self.render(constants.key_error_page)
        except ValueError:
            self.render(constants.value_error_page)


class SameStemRussianHandler(BaseHandler):
    pass


class PartSpeechHandler(BaseHandler):
    pass


class MakeMoveHandler(BaseHandler):
    pass


model = None


def main():
    global model
    model = sem.load_w2v_model(constants.WORD2VEC_MODEL_FILE)

    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()


if __name__ == "__main__":
    main()
