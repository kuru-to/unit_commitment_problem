module SlackAPIs
import Slack: sendtoslack
using TOML

abstract type ISlackApi end

function notify(slack_api::ISlackApi, text::String) end

function notify_mentioned(slack_api::ISlackApi, text::String) end

function notify_error(slack_api::ISlackApi) end

struct EmptySlack <: ISlackApi end

struct SlackApi <: ISlackApi
    endpoint::String
    notified_user::String
end

function notify(slack_api::SlackApi, text::String)
    sendtoslack(text, slack_api.endpoint)
end

function notify_mentioned(slack_api::SlackApi, text::String)
    user = slack_api.notified_user
    message = "<@$user>$text"
    notify(slack_api, message)
end

function notify_error(slack_api::SlackApi)
    error_backtrace = backtrace()
    error_msg = ":no_entry_sign: Ocurred error! ```$error_backtrace```"
    notify(slack_api, error_msg)
end


function get_slack_api()
    filename_config = "config/config_slack.ini"
    config_section = "DEFAULT"

    if !isfile(filename_config)
        return EmptySlack()
    end

    conf = TOML.parsefile(filename_config)
    endpoint = conf[config_section]["SLACK_API_ENDPOINT"]
    mention_user = conf[config_section]["MENTIONED_ID"]
    SlackApi(endpoint, mention_user)
end

end
