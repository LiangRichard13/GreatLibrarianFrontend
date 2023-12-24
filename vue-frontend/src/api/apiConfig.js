import service from "@/utils/request";

export function findApiKeyByUserId(id) {
    return service({
        url: '/APIKey',
        method: 'get',
        params: {
            uid: id
        }
    })
}

export function deleteById(data) {
    return service({
        url: '/APIKey',
        method: 'delete',
        data:data
    })
}

export function addApiKey(data) {
    return service({
        url: '/APIKey',
        method: 'post',
        data: data
    })
}