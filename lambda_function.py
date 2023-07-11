# -*- coding: utf-8 -*-
# This sample demonstrates handling intents from an Alexa skill using the Alexa Skills Kit SDK for Python.
# Please visit https://alexa.design/cookbook for additional examples on implementing slots, dialog management,
# session persistence, api calls, and more.
# This sample is built using the handler classes approach in skill builder.
import logging
import ask_sdk_core.utils as ask_utils
import os
from ask_sdk_core.skill_builder import SkillBuilder
from ask_sdk_core.dispatch_components import AbstractRequestHandler
from ask_sdk_core.dispatch_components import AbstractExceptionHandler
from ask_sdk_core.handler_input import HandlerInput
from ask_sdk_model import ui
from ask_sdk_model.interfaces.audioplayer import PlayDirective, PlayBehavior, AudioItem, Stream
from ask_sdk_model.interfaces.alexa.presentation.apl import RenderDocumentDirective
from utils import create_presigned_url
from ask_sdk_model import Response
import requests
import json


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
sessionID = None
botID = 'bo-f907773e-9730-4167-88ff-4079014f40e8'
clientKey = 's-ea0e0c08-2dd3-4152-bc58-175c5f32603f'
botName = 'EVA Alexa POC'
botID1 = 'bo-f907773e-9730-4167-88ff-4079014f40e8'
clientKey1 = 's-ea0e0c08-2dd3-4152-bc58-175c5f32603f'
botName1 = 'EVA Alexa POC'

class LaunchRequestHandler(AbstractRequestHandler):
    """Handler for Skill Launch."""

    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool

        return ask_utils.is_request_type("LaunchRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speak_output = "Welcome to Hello World Skill! How can I help you?"
        url = "https://eva-replica.hellojio.jio.com/jiointeract/api/v1/session/create"
        global botName
        global botID
        global clientKey
        # bn = handler_input.request_envelope.request.intent.slots['BotName'].resolutions.resolutions_per_authority[0].values[0].value.name
        # bid = handler_input.request_envelope.request.intent.slots['BotID'].resolutions.resolutions_per_authority[0].values[0].value.name
        # if bn is not None and bid is not None:
        #     botName = bn
        #     botID = bid
        # print(f'bot name : {bn} {botName1}')
        # print(f'bot id : {bid} {botID1}')
        payload = json.dumps({
            "botName": botName1,
            "botId": botID,
            "clientKey": clientKey,
            "context": "default",
            "botResponseType": "Text | Audio",
            "language": "en",
            "user": {
                "ani": "7020142110"
            }
        })
        headers = {
            'Content-Type': 'application/json'
        }

        res = requests.request("POST", url, headers=headers, data=payload)
        res = json.loads(res.text)
        print(handler_input.attributes_manager.request_attributes)
        print('entered')
        global sessionID
        sessionID = res["sessionId"]
        return (
            handler_input.response_builder
            .speak(speak_output)
            .ask(speak_output)
            .response
        )


class CreateSessionIntentHandler(AbstractRequestHandler):
    """Handler for Hello World Intent."""

    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        # print('entered')
        return ask_utils.is_intent_name("CreateSession")(handler_input)

    def handle(self, handler_input):
        url = "https://eva-replica.hellojio.jio.com/jiointeract/api/v1/session/create"
        global botName
        global botID
        global clientKey
        # bn = handler_input.request_envelope.request.intent.slots['BotName'].resolutions.resolutions_per_authority[0].values[0].value.name
        # bid = handler_input.request_envelope.request.intent.slots['BotID'].resolutions.resolutions_per_authority[0].values[0].value.name
        # if bn is not None and bid is not None:
        #     botName = bn
        #     botID = bid
        # print(f'bot name : {bn} {botName1}')
        # print(f'bot id : {bid} {botID1}')
        payload = json.dumps({
            "botName": botName1,
            "botId": botID,
            "clientKey": clientKey,
            "context": "default",
            "botResponseType": "Text | Audio",
            "language": "en",
            "user": {
                "ani": "7020142110"
            }
        })
        headers = {
            'Content-Type': 'application/json'
        }

        res = requests.request("POST", url, headers=headers, data=payload)
        res = json.loads(res.text)
        print(handler_input.attributes_manager.request_attributes)
        print('entered')
        global sessionID
        sessionID = res["sessionId"]
        speech_output = 'Bot connection has been established. Please enter your query'
        return (
            handler_input.response_builder
            .speak(speech_output)
            .ask(speech_output)
            .response
        )


class EndSessionIntentHandler(AbstractRequestHandler):
    """Handler for Hello World Intent."""

    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        # print('entered')
        return ask_utils.is_intent_name("EndSession")(handler_input)

    def handle(self, handler_input):
        global sessionID
        if sessionID is None:
            speech_output = 'No session is active. Kindly start the session before ending it.'
            return (
                handler_input.response_builder
                .speak(speech_output)
                .ask(speech_output)
                .response
            )

        url = f"https://eva-replica.hellojio.jio.com/jiointeract/api/v1/session/end?sessionId={sessionID}"

        payload = ""
        headers = {}

        res = requests.request("POST", url, headers=headers, data=payload)
        res = json.loads(res.text)
        print(handler_input.attributes_manager.request_attributes)
        print('entered')
        speech_output = res["message"]
        return (
            handler_input.response_builder
            .speak(speech_output)
            .ask(speech_output)
            .response
        )



class BotQueryIntentHandler(AbstractRequestHandler):
    """Handler for Hello World Intent."""

    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        # print('entered')
        return ask_utils.is_intent_name("BotQuery")(handler_input)

    def handle(self, handler_input):
        global sessionID
        if sessionID is None:
            speech_output = 'Bot connection has not been established. Please initiate before entering your query'
            return (
                handler_input.response_builder
                .speak(speech_output)
                .ask(speech_output)
                .response
            )
        url = f"https://eva-replica.hellojio.jio.com/jiointeract/api/v2/bot/statement?sessionId" \
              f"={sessionID}"
        
        payload = json.dumps({
            "query": handler_input.request_envelope.request.intent.slots['UserQuery'].value,
            "lang": "en",
            "mode": "Audio"
        })
        headers = {
            'Content-Type': 'application/json'
        }
        
        res = requests.request("POST", url, headers=headers, data=payload)
        res = json.loads(res.text)
        intent = res["action"]["intent"]
        # mp3_url = "https://hellojiodiag.blob.core.windows.net/eva/SIT/EVA-Enterprise/up-173d1ee2-b452-4992-9c6c-82b67e1777fc.mp3?type=audio/mpeg"
        mp3_url = create_presigned_url(f"Media/{intent}.mp3")
        mp3_url = mp3_url.replace('&', '&amp;')
        # mp3_url = 'soundbank://soundlibrary/water/nature/nature_08'
        # te = 'Response played'
        speech_output = ("<audio src=\"{}\"></audio>").format(mp3_url)
        display_text = res["action"]["modes"][1]["textData"]

        apl_document = {
                          "type": "APL",
                          "version": "2023.1",
                          "mainTemplate": {
                            "item": {
                              "type": "Text",
                              "text": display_text,
                              "fontSize": "30px",
                              "fontStyle" : "italic",
                              "color" : "beige"
                            }
                          }
                        }
        directive = RenderDocumentDirective(
            token="new_token", document=apl_document)

        handler_input.response_builder.add_directive(directive)
        handler_input.response_builder.speak(speech_output)

        return handler_input.response_builder.response
        # return (
        #     handler_input.response_builder
        #     .speak(speech_output)
        #     .ask(speech_output)
        #     .set_card(ui.SimpleCard(title="Visual Response", content=display_text))
        #     .response
        #     )
        # response = {
        #     'version': '1.0',
        #     'response': {
        #         'directives': [
        #             {
        #                 'type': 'AudioPlayer.Play',
        #                 'playBehavior': 'REPLACE_ALL',
        #                 'audioItem': {
        #                     'stream': {
        #                         'token': 'unique_token',
        #                         'url': mp3_url,
        #                         'offsetInMilliseconds': 0
        #                     }
        #                 }
        #             }
        #         ],
        #         'shouldEndSession': False
        #     }
        # }

        # return {
        #     'statusCode': 200,
        #     'body': json.dumps(response)
        # }

        # url = f"https://eva-replica.hellojio.jio.com/jiointeract/api/v2/bot/statement?sessionId" \
        #       f"={sessionID}"
        #
        # payload = json.dumps({
        #     "query": handler_input.request_envelope.request.intent.slots['UserQuery'].value,
        #     "lang": "en",
        #     "mode": "Text"
        # })
        # headers = {
        #     'Content-Type': 'application/json'
        # }
        #
        # res = requests.request("POST", url, headers=headers, data=payload)
        # res = json.loads(res.text)
        # # print(handler_input.attributes_manager.request_attributes)
        # print('entered bot query')
        # print(res)
        # text = res["action"]["modes"][0]["textData"]
        # speech_output = text
        # return (
        #     handler_input.response_builder
        #     .speak(speech_output)
        #     .ask(speech_output)
        #     .response
        # )


class HelpIntentHandler(AbstractRequestHandler):
    """Handler for Help Intent."""

    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("AMAZON.HelpIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speak_output = "You can say hello to me! How can I help?"

        return (
            handler_input.response_builder
            .speak(speak_output)
            .ask(speak_output)
            .response
        )


class CancelOrStopIntentHandler(AbstractRequestHandler):
    """Single handler for Cancel and Stop Intent."""

    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return (ask_utils.is_intent_name("AMAZON.CancelIntent")(handler_input) or
                ask_utils.is_intent_name("AMAZON.StopIntent")(handler_input))

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speak_output = "Goodbye!"

        return (
            handler_input.response_builder
            .speak(speak_output)
            .response
        )


class FallbackIntentHandler(AbstractRequestHandler):
    """Single handler for Fallback Intent."""

    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("AMAZON.FallbackIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        logger.info("In FallbackIntentHandler")
        speech = "Hmm, I'm not sure. You can say Hello or Help. What would you like to do?"
        reprompt = "I didn't catch that. What can I help you with?"

        return handler_input.response_builder.speak(speech).ask(reprompt).response


class SessionEndedRequestHandler(AbstractRequestHandler):
    """Handler for Session End."""

    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_request_type("SessionEndedRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response

        # Any cleanup logic goes here.

        return handler_input.response_builder.response


class IntentReflectorHandler(AbstractRequestHandler):
    """The intent reflector is used for interaction model testing and debugging.
    It will simply repeat the intent the user said. You can create custom handlers
    for your intents by defining them above, then also adding them to the request
    handler chain below.
    """

    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_request_type("IntentRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        intent_name = ask_utils.get_intent_name(handler_input)
        speak_output = "You just triggered " + intent_name + "."

        return (
            handler_input.response_builder
            .speak(speak_output)
            # .ask("add a reprompt if you want to keep the session open for the user to respond")
            .response
        )


class CatchAllExceptionHandler(AbstractExceptionHandler):
    """Generic error handling to capture any syntax or routing errors. If you receive an error
    stating the request handler chain is not found, you have not implemented a handler for
    the intent being invoked or included it in the skill builder below.
    """

    def can_handle(self, handler_input, exception):
        # type: (HandlerInput, Exception) -> bool
        return True

    def handle(self, handler_input, exception):
        # type: (HandlerInput, Exception) -> Response
        logger.error(exception, exc_info=True)

        speak_output = "Sorry, I had trouble doing what you asked. Please try again."

        return (
            handler_input.response_builder
            .speak(speak_output)
            .ask(speak_output)
            .response
        )


# The SkillBuilder object acts as the entry point for your skill, routing all request and response
# payloads to the handlers above. Make sure any new handlers or interceptors you've
# defined are included below. The order matters - they're processed top to bottom.


sb = SkillBuilder()

sb.add_request_handler(LaunchRequestHandler())
sb.add_request_handler(CreateSessionIntentHandler())
sb.add_request_handler(BotQueryIntentHandler())
sb.add_request_handler(EndSessionIntentHandler())
sb.add_request_handler(HelpIntentHandler())
sb.add_request_handler(CancelOrStopIntentHandler())
sb.add_request_handler(FallbackIntentHandler())
sb.add_request_handler(SessionEndedRequestHandler())
sb.add_request_handler(
    IntentReflectorHandler())  # make sure IntentReflectorHandler is last so it doesn't override your custom intent handlers

sb.add_exception_handler(CatchAllExceptionHandler())

lambda_handler = sb.lambda_handler()

# with open('input.json', 'r') as file:
#     json_data = json.load(file)
# response = lambda_handler(json_data, None)
# print(response)

