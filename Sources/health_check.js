const slack = require("./slack.js");
const request = require("request-promise-native");
const env = Object.create(process.env);

const healthCheckURL = env.HEALTH_CHECK_URL;

const main = async () => {
    const options = {
        uri: healthCheckURL,
        method: "GET",
        json: true,
        resolveWithFullResponse: true,
        timeout: 1000
    }
    try {
        const response = await request(options);

        if (response.statusCode === 200) {
            var message = '✅✅✅✅ Health check 성공 ✅✅✅✅'
            console.log(message);
        } else {
            var message = '🚨🚨🚨🚨 Health check 실패 🚨🚨🚨🚨  <@U02FRDDT8KV> <@U02FRDHU02E> <@U02FNDA6E2Z> <@U04C3LL4VJ5> <@U02FJM0FA06>' + env.HEALTH_CHECK_URL
            slack.post(message);
            throw new Error("Health check failed");
        }
    } catch (err) {
        console.log(err);
    }
};

main();
