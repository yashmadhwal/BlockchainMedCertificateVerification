pragma solidity <0.6.5;

contract MOSGOVCOVIDQR{

    address public healthMinistry;

    uint public hospitalId;
    uint public vaccineCard;

    constructor() public {
        healthMinistry = msg.sender;
        hospitalId = 1;
        vaccineCard = 1;
    }

    mapping (address => HospitalClinic) public HospitalRegistry;
    struct HospitalClinic{
        uint registrationCertificate;
        string name;

        address hospitalAddress;

        string vaccineName;
        bool registeredVacciner;

        uint _numberOfVaccinesRollOut;
    }

    mapping (uint => PublicRegistryOR) public PublicBook;
    struct PublicRegistryOR{

        // QR information
        uint vaccineCardSerialNumber;
        string patientName;
        uint dateOfVaccination; // from Blockchain

        // Hospital information
        uint registrationCertificate;
        string name;
        address hospitalAddress;
        string vaccineName;

    }


    function registerHospital(address _hospitalAddress, string memory _hospitalName) public onlyOwner{
        require(HospitalRegistry[_hospitalAddress].registeredVacciner == false,"Hospital Already Registered!");
        HospitalRegistry[_hospitalAddress] = HospitalClinic(hospitalId,_hospitalName,_hospitalAddress,'SputnikV',true,0);
        hospitalId++;
    }

    function VaccinatePeople() public onlyRegisteredHospital{
        // attaining hospital's information
        uint _registrationCertificate = HospitalRegistry[msg.sender].registrationCertificate;
        string memory _hospitalName = HospitalRegistry[msg.sender].name;
        address _hopitalAddress = HospitalRegistry[msg.sender].hospitalAddress;
        string memory _vaccineName = HospitalRegistry[msg.sender].vaccineName;

        PublicBook[vaccineCard] = PublicRegistryOR(vaccineCard,'SomeName',now,_registrationCertificate,_hospitalName,_hopitalAddress,_vaccineName);

        // increment Vaccine RollOuts
        HospitalRegistry[msg.sender]._numberOfVaccinesRollOut++;
        vaccineCard ++;
    }

    modifier onlyOwner(){
        require(healthMinistry == msg.sender,'Invalid Access!');
        _;
    }

    modifier onlyRegisteredHospital(){
        require(HospitalRegistry[msg.sender].registeredVacciner == true, 'Only Registered hospitals!');
        _;
    }

}
