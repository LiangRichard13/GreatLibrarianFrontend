import service from "@/utils/request";

export function getExperimentProgress(expId) {
    return service({
        url: '/progress',
        method: 'get',
        params: {
            tPid: expId,
        }
    })
}

export function updateExperimentStatus(data) {
    return service({
        url: '/QA',
        method: 'post',
        data:data
    })
}

export function startExp(data) {
    return service({
        url: '/testProjectOperation',
        method: 'post',
        params:data
    })
}

export function genReport(tPid) {
    return service({
        url: '/testProjectOperation',
        method: 'put',
        params:{tPid:tPid}
    })
}