pragma solidity ^0.5.0;

contract Faccount {
    
    struct facc {
        uint fm_id;
        string fName;
        string lName;
        string doc1_hash;
        string doc2_hash;
        string doc3_hash;
        string doc4_hash;
    }
    string test;
    mapping (uint => facc) farmer_accounts;
    uint[] public farmerAccts;
    
    constructor() public{
        test=" ";
    }
    function setFarmer(uint _fm_id, string memory _fName, string memory _lName, string memory _doc1_hash, string memory _doc2_hash, string memory _doc3_hash, string memory _doc4_hash) public {
        facc storage farmer = farmer_accounts[_fm_id];
        
        farmer.fName = _fName;
        farmer.lName = _lName;
        farmer.fm_id = _fm_id;
        farmer.doc1_hash = _doc1_hash;
        farmer.doc2_hash = _doc2_hash;
        farmer.doc3_hash = _doc3_hash;
        farmer.doc4_hash = _doc4_hash;
        
        
        farmerAccts.push(_fm_id) -1;
    }
    
    function getFarmer() view public returns(uint[] memory) {
        return farmerAccts;
    }
    
    function getFarmer(uint _fm_id) view public returns (uint, string memory, string memory, string memory, string memory, string memory, string memory) {
        return (farmer_accounts[_fm_id].fm_id, farmer_accounts[_fm_id].fName, farmer_accounts[_fm_id].lName, farmer_accounts[_fm_id].doc1_hash, farmer_accounts[_fm_id].doc2_hash, farmer_accounts[_fm_id].doc3_hash, farmer_accounts[_fm_id].doc4_hash);
    }
    
    function countFarmer() view public returns (uint) {
        return farmerAccts.length;
    }
    
}