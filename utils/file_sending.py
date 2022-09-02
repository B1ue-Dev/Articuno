"""
file_sending
GitHub: https://github.com/interactions-py/enhanced/blob/main/interactions/ext/enhanced/file_sending.py
(c) 2022 interactions-py.
"""
from typing import List, Optional, Union

from aiohttp import MultipartWriter
from interactions.api.http.route import Route
from interactions.client.context import CommandContext, ComponentContext, _Context
from interactions.client.models.component import _build_components

from interactions import (
    MISSING,
    ActionRow,
    Button,
    Embed,
    File,
    InteractionCallbackType,
    Message,
    MessageInteraction,
    SelectMenu,
)


# file sending
async def create_interaction_response(
    self, token: str, application_id: int, data: dict, files: List[File]
) -> None:
    """
    Posts initial response to an interaction, but you need to add the token.
    :param token: Token.
    :param application_id: Application ID snowflake
    :param data: The data to send.
    """

    file_data = None
    if files:
        file_data = MultipartWriter("form-data")
        part = file_data.append_json(data)
        part.set_content_disposition("form-data", name="payload_json")
        data = None

        for id, file in enumerate(files):
            part = file_data.append(
                file._fp,
            )
            part.set_content_disposition(
                "form-data", name=f"files[{str(id)}]", filename=file._filename
            )

    return await self._req.request(
        Route("POST", f"/interactions/{application_id}/{token}/callback"),
        json=data,
        data=file_data,
    )


async def edit_interaction_response(
    self,
    data: dict,
    files: List[File],
    token: str,
    application_id: str,
    message_id: str = "@original",
) -> dict:
    """
    Edits an existing interaction message, but token needs to be manually called.
    :param data: A dictionary containing the new response.
    :param token: the token of the interaction
    :param application_id: Application ID snowflake.
    :param message_id: Message ID snowflake. Defaults to `@original` which represents the initial response msg.
    :return: Updated message data.
    """
    # ^ again, I don't know if python will let me
    file_data = None
    if files:
        file_data = MultipartWriter("form-data")
        part = file_data.append_json(data)
        part.set_content_disposition("form-data", name="payload_json")
        data = None

        for id, file in enumerate(files):
            part = file_data.append(
                file._fp,
            )
            part.set_content_disposition(
                "form-data", name=f"files[{str(id)}]", filename=file._filename
            )

    return await self._req.request(
        Route("PATCH", f"/webhooks/{application_id}/{token}/messages/{message_id}"),
        json=data,
        data=file_data,
    )


async def base_send(
    self,
    content: Optional[str] = MISSING,
    *,
    tts: Optional[bool] = MISSING,
    files: Optional[List[File]] = None,
    embeds: Optional[Union[Embed, List[Embed]]] = MISSING,
    allowed_mentions: Optional[MessageInteraction] = MISSING,
    components: Optional[
        Union[
            ActionRow,
            Button,
            SelectMenu,
            List[ActionRow],
            List[Button],
            List[SelectMenu],
        ]
    ] = MISSING,
    ephemeral: Optional[bool] = False,
) -> Message:
    if (
        content is MISSING
        and self.message
        and self.callback == InteractionCallbackType.DEFERRED_UPDATE_MESSAGE
    ):
        _content = self.message.content
    else:
        _content: str = "" if content is MISSING else content
    _tts: bool = False if tts is MISSING else tts
    # _file = None if file is None else file
    # _attachments = [] if attachments else None
    if (
        embeds is MISSING
        and self.message
        and self.callback == InteractionCallbackType.DEFERRED_UPDATE_MESSAGE
    ):
        embeds = self.message.embeds
    _embeds: list = (
        []
        if not embeds or embeds is MISSING
        else (
            [embed._json for embed in embeds]
            if isinstance(embeds, list)
            else [embeds._json]
        )
    )
    _allowed_mentions: dict = {} if allowed_mentions is MISSING else allowed_mentions
    if components is not MISSING and components:
        # components could be not missing but an empty list
        _components = _build_components(components=components)
    elif (
        components is MISSING
        and self.message
        and self.callback == InteractionCallbackType.DEFERRED_UPDATE_MESSAGE
    ):
        if isinstance(self.message.components, list):
            _components = self.message.components
        else:
            _components = [self.message.components]
    else:
        _components = []

    if not files or files is MISSING:
        _files = []
    elif isinstance(files, list):
        _files = [file._json_payload(id) for id, file in enumerate(files)]
    else:
        _files = [files._json_payload(0)]
        files = [files]

    _ephemeral: int = (1 << 6) if ephemeral else 0

    # TODO: post-v4: Add attachments into Message obj.
    payload: Message = Message(
        content=_content,
        tts=_tts,
        # files=file,
        attachments=_files,
        embeds=_embeds,
        allowed_mentions=_allowed_mentions,
        components=_components,
        flags=_ephemeral,
    )
    self.message = payload
    self.message._client = self.client
    return payload, files


async def command_send(self, content: Optional[str] = MISSING, **kwargs) -> Message:
    payload, files = await base_send(self, content, **kwargs)

    if not self.deferred:
        self.callback = InteractionCallbackType.CHANNEL_MESSAGE_WITH_SOURCE

    _payload: dict = {"type": self.callback.value, "data": payload._json}

    msg = None
    if self.responded or self.deferred:
        if self.deferred:
            res = await edit_interaction_response(
                self.client,
                data=payload._json,
                files=files,
                token=self.token,
                application_id=str(self.application_id),
            )
            self.deferred = False
            self.responded = True
        else:
            res = await self.client._post_followup(
                data=payload._json,
                token=self.token,
                application_id=str(self.application_id),
            )
        self.message = msg = Message(**res, _client=self.client)
    else:
        res = await create_interaction_response(
            self.client,
            token=self.token,
            application_id=int(self.id),
            data=_payload,
            files=files,
        )
        if res and not res.get("code"):
            # if sending message fails somehow
            self.message = msg = Message(**res, _client=self.client)
        self.responded = True
    if msg is not None:
        return msg
    return payload


async def component_send(self, content: Optional[str] = MISSING, **kwargs) -> Message:
    payload, files = await base_send(self, content, **kwargs)

    if not self.deferred:
        self.callback = InteractionCallbackType.CHANNEL_MESSAGE_WITH_SOURCE
    _payload: dict = {"type": self.callback.value, "data": payload._json}
    msg = None
    if (
        self.responded
        or self.deferred
        or self.callback == InteractionCallbackType.DEFERRED_UPDATE_MESSAGE
    ):
        if self.deferred:
            res = await edit_interaction_response(
                self.client,
                data=payload._json,
                files=files,
                token=self.token,
                application_id=str(self.application_id),
            )
            self.deferred = False
            self.responded = True
        else:
            res = await self.client._post_followup(
                data=payload._json,
                token=self.token,
                application_id=str(self.application_id),
            )
        self.message = msg = Message(**res, _client=self.client)
    else:
        await create_interaction_response(
            self.client,
            token=self.token,
            application_id=int(self.id),
            data=_payload,
            files=files,
        )
        __newdata = await edit_interaction_response(
            self.client,
            data={},
            token=self.token,
            application_id=str(self.application_id),
            files=files,
        )
        if __newdata and not __newdata.get("code"):
            # if sending message fails somehow
            msg = Message(**__newdata, _client=self.client)
            self.message = msg
        self.responded = True
    if msg is not None:
        return msg
    return payload


_Context.send = base_send
CommandContext.send = command_send
ComponentContext.send = component_send
