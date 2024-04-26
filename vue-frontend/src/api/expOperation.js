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

export function errorHandle(expId) {
    return service({
        url: '/progress',
        method: 'post',
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

export function updateReport(tPid) {
    return service({
        url: '/testProjectOperation',
        method: 'put',
        params:{tPid:tPid}
    })
}

export function genReport(tPid,num) {
    return service({
        url: '/testProjectOperation',
        method: 'get',
        params:{tPid:tPid,n:num,choose:2}
    })
}

export function getReportNum(tPid){
    return service({
        url: '/testProjectOperation',
        method: 'get',
        params:{tPid:tPid,choose:1}
    })
}

export function getInteraction(id,type) {
    return service({
        url: '/testProjectOperation',
        method: 'delete',
        params: {tPid:id},
        data:{type:type}
    })
}