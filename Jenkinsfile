// All stages:
STAGE_ONE = 'stage one'
STAGE_TWO = 'stage two'
STAGE_THREE = 'stage three'
STAGE_PARALLEL = 'parallel stages'

RUN_ALL_STAGES = 'All stages'
RUN_TOOLCHAIN_JOB = 'Toolchain job'
RUN_TEST_NIGHTLY_JOB = 'Test nightly job'

// stage statuses:
STAGE_SUCCESS = "SUCCESS"
STAGE_UNSUCCESSFUL = "NOT SUCCESS"

// Used to store the status of every stage
STG_RUN = 0
STG_RESULT = 1

TESTS = [
    STAGE2_RAN: false,
    STAGE3_RAN: false
]


def triggerBuildChildJob(jobName, pars, propagateResult=false) {
    echo 'Setting up remote job:'
    echo jobName
    def dsJob = build job: jobName, parameters: pars, propagate: propagateResult, wait: true
    return dsJob
}

def buildTriggerIsUser() {
    return currentBuild.getBuildCauses('hudson.model.Cause$UserIdCause')
}

pipeline {
    agent any

    environment {
        CURRENT_BUILD_ID = "${currentBuild.projectName}-${currentBuild.id}"
    }
    
    parameters {
        choice(
            name: 'STAGES_TO_RUN',
            choices: ["${RUN_ALL_STAGES}", "${RUN_TOOLCHAIN_JOB}", "${RUN_TEST_NIGHTLY_JOB}"],
            description: 'Select the stages to run for this pipeline'
        )
        booleanParam(
            name: 'SKIP',
            defaultValue: false,
            description: 'If checked child jobs will not run and pipeline result will be set as SUCCESS'
        )
    }
    
    stages {
        stage (STAGE_ONE) {
            steps {
                script {
                    echo 'This step is only for preparation'
                    if (buildTriggerIsUser()) {
                        echo 'Triggered by user'
                        // Unstash status of previous run
                        def buildName = currentBuild.projectName
                        echo "The buildName is: ${buildName}"
                        def prevBuildId = Jenkins.instance.getItem("${buildName}").lastFailedBuild.displayName.substring(1)
                        // prevBuildId = prevBuildId.subString(1)
                        // "https://eeb4-201-166-189-50.ngrok-free.app/job//ParentPipeline/lastFailedBuild/buildNumber"
                        echo "The prevBuildId is: ${prevBuildId}"
                        // unstash "ParentPipelineStash"
                        // Logic to decide what to run
                        echo "${buildName}-${prevBuildId}"
                    }
                    
                    echo 'Triggered by timer'
                    def stgOnePars = [
                        string(name: 'Name', value: 'Olivia'),
                        string(name: 'nickName', value: 'Miniatura')
                    ]
                    def childJob = triggerBuildChildJob('ChildPipeline', stgOnePars)
                    env.CHILD_JOB_URL = childJob.absoluteUrl
                    env.RELEASE_BUILD_JOB_NUMBER = childJob.number
                    env.RELEASE_BUILD_JOB_DISPLAY_NAME = childJob.displayName
                    if (childJob.result != 'SUCCESS') {
                        sh "exit 1"
                    }
                    
                }
            }
            post {
                always {
                    storeDataToStash("${CURRENT_BUILD_ID}")
                }
                success {
                    appendToFile("${CURRENT_BUILD_ID}", "${STAGE_ONE}", "${STAGE_SUCCESS}" )
                }
                unsuccessful {
                    appendToFile("${CURRENT_BUILD_ID}", "${STAGE_ONE}", "${STAGE_UNSUCCESSFUL}" )
                }
            }
        }
        
        stage (STAGE_PARALLEL) {
            parallel {
                stage (STAGE_TWO) {
                    when {
                        expression {
                            !(params.SKIP) && (params.STAGES_TO_RUN == "${RUN_ALL_STAGES}" || params.STAGES_TO_RUN == "${RUN_TOOLCHAIN_JOB}")
                        }
                    }
                    steps {
                        script {
                            echo 'This step is parallel job 1'
                            def stgTwoPars = [
                                string(name: 'Nombre', value: 'Andres'),
                                string(name: 'sobreNombre', value: 'Changs')
                            ]
                            def childJob = triggerBuildChildJob('ChildPipeline2', stgTwoPars)
                            TESTS.STAGE2_RAN = true
                            if (childJob.result != 'SUCCESS') {
                                sh "exit 0"
                            }
                        }
                    }
                    post {
                        always {
                            echo 'Nada'
                        }
                        success {
                            appendToFile("${CURRENT_BUILD_ID}", "${STAGE_TWO}", "${STAGE_SUCCESS}")
                        }
                        unsuccessful {
                            appendToFile("${CURRENT_BUILD_ID}", "${STAGE_TWO}", "${STAGE_UNSUCCESSFUL}")
                        }
                    }
                }
                
                stage (STAGE_THREE) {
                    when {
                        expression {
                            !(params.SKIP) && (params.STAGES_TO_RUN == "${RUN_ALL_STAGES}" || params.STAGES_TO_RUN == "${RUN_TEST_NIGHTLY_JOB}")
                        }
                    }
                    steps {
                        script {
                            echo 'This step is parallel job 2'
                            def stgThreePars = [
                                string(name: 'Nombre', value: 'Elisa'),
                                string(name: 'Apodo', value: 'Elixir')
                            ]
                            catchError(message: 'STAGE_THREE failed', buildResult: 'UNSTABLE', stageResult: 'FAILURE') {
                                def childJob = triggerBuildChildJob('ChildPipeline3', stgThreePars)
                                TESTS.STAGE3_RAN = true
                                sh "exit 0"
                            }
                        }
                    }
                    post {
                        always {
                            echo 'Nada'
                        }
                        success {
                            appendToFile("${CURRENT_BUILD_ID}", "${STAGE_THREE}", "${STAGE_SUCCESS}")
                        }
                        unsuccessful {
                            appendToFile("${CURRENT_BUILD_ID}", "${STAGE_THREE}", "${STAGE_UNSUCCESSFUL}")
                        }
                    }
                }
            }
        }
        
        stage('Promote') {
            /*when {
                expression {
                    TESTS.STAGE2_RAN && TESTS.STAGE3_RAN && !(currentBuild.result in ["UNSTABLE", "FAILURE", "ABORTED"])
                }
            }*/
            steps {
                echo "All done and all run"
                echo currentBuild.result
            }
        }
    }
    post {
        always {
            sh "cat ${CURRENT_BUILD_ID}"
            stash includes: "${CURRENT_BUILD_ID}", name: "ParentPipelineStash"
        }
    }
}
