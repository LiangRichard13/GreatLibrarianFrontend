import service from "@/utils/request";

export function findByUserId(id) {
    return service({
        url: '/dataSetConfig/findByUserId',
        method: 'get',
           params: {
            id: id
        }
    })
}
export function deleteById(id) {
    return service({
        url: '/dataSetConfig/deleteById',
        method: 'delete',
           params: {
            id: id
        }
    })
}

export function addDateSet(data) {
    return service({
        url: '/dataSetConfig/addApiKey',
        method: 'post',
        data: data
    })
}