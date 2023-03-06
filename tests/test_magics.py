from unittest import mock

from genai import generate


@mock.patch(
    "openai.ChatCompletion.create",
    return_value={
        "choices": [
            {
                "message": {
                    "role": "assistant",
                    "content": "Here's a suggestion",
                },
            },
        ],
    },
    autospec=True,
)
def test_assist_magic(create, ip):
    ip.run_cell_magic(magic_name="assist", line="", cell="create a scatterplot from df")

    # Check that create was called with the correct arguments
    create.assert_called_once_with(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": generate.NOTEBOOK_CODING_ASSISTANT_TEMPLATE,
            },
            {
                "role": "user",
                "content": "create a scatterplot from df",
            },
        ],
    )


@mock.patch(
    "openai.ChatCompletion.create",
    return_value={
        "choices": [
            {
                "message": {
                    "role": "assistant",
                    "content": "just like code better",
                },
            },
        ],
    },
    autospec=True,
)
def test_assist_magic_with_args(create, ip):
    ip.set_next_input = mock.MagicMock()

    ip.run_cell_magic(
        magic_name="assist",
        line="--in-place --verbose",
        cell="create a scatterplot from df",
    )

    # Check that create was called with the correct arguments
    create.assert_called_once_with(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": generate.NOTEBOOK_CODING_ASSISTANT_TEMPLATE,
            },
            {
                "role": "user",
                "content": "create a scatterplot from df",
            },
        ],
    )

    ip.set_next_input.assert_called_once_with(
        "#%%assist --in-place --verbose\ncreate a scatterplot from df\njust like code better",
        replace=True,
    )


@mock.patch(
    "openai.ChatCompletion.create",
    return_value={
        "choices": [
            {
                "message": {
                    "role": "assistant",
                    "content": "superplot(df)",
                },
            },
        ],
    },
    autospec=True,
)
def test_assist_magic_with_fresh_arg(create, ip):
    ip.set_next_input = mock.MagicMock()

    ip.run_cell_magic(
        magic_name="assist",
        line="--fresh",
        cell="create a scatterplot from df",
    )

    create.assert_called_once_with(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": generate.NOTEBOOK_CODING_ASSISTANT_TEMPLATE,
            },
            # Note that there is zero other context, due to running with --fresh
            {
                "role": "user",
                "content": "create a scatterplot from df",
            },
        ],
    )

    ip.set_next_input.assert_called_once_with(
        "create a scatterplot from df\nsuperplot(df)",
        replace=False,
    )
