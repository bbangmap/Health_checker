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
            var message = '✅✅✅✅ Health check 성공 ✅✅✅✅  ' + env.HEALTH_CHECK_URL
            slack.post(message);
        } else {
            var message = '🚨🚨🚨🚨 Health check 실패 🚨🚨🚨🚨  ' + env.HEALTH_CHECK_URL
            slack.post(message);
            throw new Error("Health check failed");
        }
    } catch (err) {
        console.log(err);
    }
};

main();