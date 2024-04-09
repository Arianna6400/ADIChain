// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract HealthCareRecords {
    struct Medic {
        string name;
        string specialization;
        bool isRegistered;
        uint256 offChainId; // Identificatore correlato al database off-chain
    }
    
    struct Patient {
        string name;
        bool isRegistered;
        uint256 offChainId; // Identificatore correlato al database off-chain
        mapping(address => bool) authorizedMedics;
    }

    // Mapping per gli hash di Reports e TreatmentPlans
    mapping(bytes32 => bool) private reportHashes;
    mapping(bytes32 => bool) private treatmentPlanHashes;

    mapping(address => Medic) public medics;
    mapping(address => Patient) public patients;

    // Eventi
    event MedicRegistered(address indexed medicAddress, string name, string specialization, uint256 offChainId);
    event PatientRegistered(address indexed patientAddress, string name, uint256 offChainId);
    event AccessGranted(address indexed patientAddress, address indexed medicAddress);
    event ReportHashLogged(bytes32 reportHash);
    event TreatmentPlanHashLogged(bytes32 treatmentPlanHash);

    // Modificatori
    modifier onlyRegisteredMedic() {
        require(medics[msg.sender].isRegistered, "Medic not registered.");
        _;
    }

    modifier onlyRegisteredPatient() {
        require(patients[msg.sender].isRegistered, "Patient not registered.");
        _;
    }

    // Funzioni per la Registrazione
    function registerMedic(string memory name, string memory specialization, uint256 offChainId) public {
        require(!medics[msg.sender].isRegistered, "Medic already registered.");
        medics[msg.sender] = Medic(name, specialization, true, offChainId);
        emit MedicRegistered(msg.sender, name, specialization, offChainId);
    }
    
    function registerPatient(string memory name, uint256 offChainId) public {
        require(!patients[msg.sender].isRegistered, "Patient already registered.");
        
        // Accedi direttamente ai campi dello struct per l'aggiornamento
        Patient storage patient = patients[msg.sender];
        patient.name = name;
        patient.isRegistered = true;
        patient.offChainId = offChainId;

        emit PatientRegistered(msg.sender, name, offChainId);
    }


    // Funzioni per la Gestione di Accessi e Logs
    function grantAccessToMedic(address medicAddress) public onlyRegisteredPatient {
        require(medics[medicAddress].isRegistered, "Medic not registered.");
        patients[msg.sender].authorizedMedics[medicAddress] = true;
        emit AccessGranted(msg.sender, medicAddress);
    }

    function logReportHash(bytes32 reportHash) public onlyRegisteredMedic {
        reportHashes[reportHash] = true;
        emit ReportHashLogged(reportHash);
    }

    function logTreatmentPlanHash(bytes32 treatmentPlanHash) public onlyRegisteredMedic {
        treatmentPlanHashes[treatmentPlanHash] = true;
        emit TreatmentPlanHashLogged(treatmentPlanHash);
    }

    // Funzioni di Verifica
    function isReportHashLogged(bytes32 reportHash) public view returns (bool) {
        return reportHashes[reportHash];
    }

    function isTreatmentPlanHashLogged(bytes32 treatmentPlanHash) public view returns (bool) {
        return treatmentPlanHashes[treatmentPlanHash];
    }
}
