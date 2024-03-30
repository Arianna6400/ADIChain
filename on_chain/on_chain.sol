// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract HealthCareRecords {

    struct Medic {
        string name;
        string specialization;
        bool isRegistered;
    }
    
    struct Patient {
        string name;
        bool isRegistered;
        mapping(address => bool) authorizedMedics;
    }

    mapping(address => Medic) public medics;
    mapping(address => Patient) public patients;

    // Eventi
    event MedicRegistered(address indexed medicAddress, string name, string specialization);
    event PatientRegistered(address indexed patientAddress, string name);
    event AccessGranted(address indexed patientAddress, address indexed medicAddress);
    event CriticalEventLogged(address indexed patientAddress, string eventType, string details);

    // Modificatori
    modifier onlyRegisteredMedic() {
        require(medics[msg.sender].isRegistered, "Medic not registered.");
        _;
    }

    modifier onlyRegisteredPatient() {
        require(patients[msg.sender].isRegistered, "Patient not registered.");
        _;
    }

    // Funzioni
    function registerMedic(string memory name, string memory specialization) public {
        require(!medics[msg.sender].isRegistered, "Medic already registered.");
        medics[msg.sender] = Medic(name, specialization, true);
        emit MedicRegistered(msg.sender, name, specialization);
    }
    
    function registerPatient(string memory name) public {
        require(!patients[msg.sender].isRegistered, "Patient already registered.");
        Patient storage newPatient = patients[msg.sender];
        newPatient.name = name;
        newPatient.isRegistered = true;
        emit PatientRegistered(msg.sender, name);
    }

    function grantAccessToMedic(address medicAddress) public onlyRegisteredPatient {
        require(medics[medicAddress].isRegistered, "Medic not registered.");
        patients[msg.sender].authorizedMedics[medicAddress] = true;
        emit AccessGranted(msg.sender, medicAddress);
    }

    function logCriticalEvent(string memory eventType, string memory details, address patientAddress) public onlyRegisteredMedic {
        require(patients[patientAddress].authorizedMedics[msg.sender], "Unauthorized access.");
        emit CriticalEventLogged(patientAddress, eventType, details);
    }
}
