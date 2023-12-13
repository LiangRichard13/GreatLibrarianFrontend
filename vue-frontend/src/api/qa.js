import service from "@/utils/request";

export function getQAByExpirenceId(expId,uid) {
    return service({
        url: '/project/getQAByExpirenceId',
        method: 'get',
        params: {
            expId: expId,
            uid:uid
        }
    })
}

export function distributeToOthers(data) {
    return service({
        url: '/project/distributeToOthers',
        method: 'post',
        data:data
    })
}

export function rateQA(data) {
    return service({
        url: '/project/rateQA',
        method: 'put',
        data:data
    })
}