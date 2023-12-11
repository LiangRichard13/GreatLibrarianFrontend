import service from "@/utils/request";

export function findByUserId(id) {
    return service({
        url: '/apiConfig/findByUserId',
        method: 'get',
        params: {
            id: id
        }
    })
}

export function deleteById(id) {
    return service({
        url: '/apiConfig/deleteById',
        method: 'delete',
        params: {
            id: id
        }
    })
}

export function addApiKey(data) {
    return service({
        url: '/apiConfig/addApiKey',
        method: 'post',
        data: data
    })
}