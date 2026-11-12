"""
Unit 9: the error taxonomy. One module decides every status code.

Four kinds of failure a caller can be told about, plus `internal` for anything
we did not anticipate. Every one carries:

  kind          machine-readable, goes in the JSON body and the log
  http_status   what serve.py answers
  user_message  the ONLY text a caller sees — never the exception text
  reason        optional sub-cause (for `upstream`: api_error | rate_limited |
                quota | empty_response), kept in the log
  detail        the raw exception text, for the log only

A gate refusal is NOT an error: it is a 200 with "refused": true. An empty
*index* is `no_index`; empty *results* from a real index are a refusal.
"""


class PipelineError(Exception):
    kind = "internal"
    http_status = 500
    default_message = "Something went wrong on our side. Quote the request_id if you report it."

    def __init__(self, user_message=None, *, stage=None, reason=None, detail=None):
        self.user_message = user_message or self.default_message
        self.stage = stage
        self.reason = reason
        self.detail = detail
        self.stage_ms = None  # filled in by app.ask_pipeline when it knows
        super().__init__(self.user_message)


class BadInputError(PipelineError):
    kind = "bad_input"
    http_status = 400
    default_message = 'Send JSON with a question in it, like {"question": "is the housing lottery random?"}'


class NoIndexError(PipelineError, RuntimeError):
    # RuntimeError too, so callers written for the old bare RuntimeError still work.
    kind = "no_index"
    http_status = 503
    default_message = "No index to search yet. Run `python app.py index` first."


class ModelTimeoutError(PipelineError):
    kind = "model_timeout"
    http_status = 504
    default_message = "The model did not answer in time. Try again."


class UpstreamError(PipelineError):
    # Provider failure, rate-limit exhaustion, session quota, or an empty model
    # response. `reason` tells them apart in the log.
    kind = "upstream"
    http_status = 502
    default_message = "The model service failed to produce an answer. Try again shortly."


def classify(exc: BaseException) -> PipelineError:
    """Known types pass through; everything else becomes `internal` (500)."""
    if isinstance(exc, PipelineError):
        # ask_pipeline tags exceptions with the stage timings it had so far.
        if exc.stage_ms is None:
            exc.stage_ms = getattr(exc, "pipeline_stage_ms", None)
        if exc.stage is None:
            exc.stage = getattr(exc, "pipeline_stage", None)
        return exc
    if type(exc).__name__ == "QuotaGuard":  # generate.QuotaGuard, by name: no circular import
        err = UpstreamError(reason="quota", stage="generate", detail=str(exc))
        err.stage_ms = getattr(exc, "pipeline_stage_ms", None)
        return err
    err = PipelineError(detail=f"{type(exc).__name__}: {exc}")
    err.stage = getattr(exc, "pipeline_stage", None)
    err.stage_ms = getattr(exc, "pipeline_stage_ms", None)
    return err
