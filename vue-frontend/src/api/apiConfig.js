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

export function deleteById(id) {
    return service({
        url: '/APIKey',
        method: 'delete',
        params: {
            id: id
        }
    })
}

export function addApiKey(data) {
    return service({
        url: '/APIKey',
        method: 'post',
        data: data
    })
}