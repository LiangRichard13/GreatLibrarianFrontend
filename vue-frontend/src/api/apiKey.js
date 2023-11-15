import service from "@/utils/request";

export function findByUserId(data) {
    return service({
        url: '/apiKey/findByUserId',
        method: 'post',
        data: data
    })
}
export function deleteById(data) {
    return service({
        url: '/apiKey/deleteById',
        method: 'post',
        data: data
    })
}

export function addApiKey(data) {
    return service({
        url: '/apiKey/addApiKey',
        method: 'post',
        data: data
    })
}