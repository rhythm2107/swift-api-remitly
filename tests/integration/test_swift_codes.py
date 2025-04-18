import pytest

# Helper HQ & Branch Payloads
HQ_PAYLOAD = {
    "address": "123 Main St",
    "bankName": "Test Bank",
    "countryISO2": "US",
    "countryName": "UNITED STATES",
    "isHeadquarter": True,
    "swiftCode": "TEATUS33XXX"
}

BRANCH_PAYLOAD = {
    **HQ_PAYLOAD,
    "swiftCode": "TEATUS33ABC", # same first 8 chars but no 'XXX' (not HQ)
    "isHeadquarter": False
}

@pytest.mark.asyncio
async def test_create_and_get_swift_code(client):
    response = await client.post("/v1/swift-codes", json=HQ_PAYLOAD)
    assert response.status_code == 200

    get_resp = await client.get(f"/v1/swift-codes/{HQ_PAYLOAD['swiftCode']}")
    assert get_resp.status_code == 200
    assert get_resp.json()["swiftCode"] == HQ_PAYLOAD["swiftCode"]


@pytest.mark.asyncio
async def test_create_duplicate_swift_code(client):
    response = await client.post("/v1/swift-codes", json=HQ_PAYLOAD)
    assert response.status_code == 200

    duplicate = await client.post("/v1/swift-codes", json=HQ_PAYLOAD)
    assert duplicate.status_code == 400
    assert "already exists" in duplicate.json()["detail"].lower()

    get_response = await client.get(f"/v1/swift-codes/{HQ_PAYLOAD['swiftCode']}")
    assert get_response.status_code == 200
    assert get_response.json()["swiftCode"] == HQ_PAYLOAD["swiftCode"]


@pytest.mark.asyncio
async def test_create_lowercase_swift_rejected(client):
    bad = {**HQ_PAYLOAD, "swiftCode": HQ_PAYLOAD["swiftCode"].lower()}
    response = await client.post("/v1/swift-codes", json=bad)
    assert response.status_code == 400
    assert "must be uppercase" in response.json()["detail"]


@pytest.mark.asyncio
async def test_hq_without_xxx_rejected(client):
    bad = {**HQ_PAYLOAD, "swiftCode": BRANCH_PAYLOAD["swiftCode"]}
    response = await client.post("/v1/swift-codes", json=bad)
    assert response.status_code == 400
    assert "must end with 'XXX'" in response.json()["detail"]


@pytest.mark.asyncio
async def test_hq_returns_branches(client):
    await client.post("/v1/swift-codes", json=HQ_PAYLOAD)
    await client.post("/v1/swift-codes", json=BRANCH_PAYLOAD)

    response = await client.get(f"/v1/swift-codes/{HQ_PAYLOAD["swiftCode"]}")
    body = response.json()

    assert response.status_code == 200
    assert body["isHeadquarter"] is True
    assert len(body["branches"]) == 1
    assert body["branches"][0]["swiftCode"] == BRANCH_PAYLOAD["swiftCode"]


@pytest.mark.asyncio
async def test_get_by_country(client):
    await client.post("/v1/swift-codes", json=HQ_PAYLOAD)
    await client.post("/v1/swift-codes", json=BRANCH_PAYLOAD)

    response = await client.get(f"/v1/swift-codes/country/{HQ_PAYLOAD['countryISO2']}")
    body = response.json()

    assert response.status_code == 200
    assert body["countryISO2"] == HQ_PAYLOAD["countryISO2"]
    assert len(body["swiftCodes"]) == 2


@pytest.mark.asyncio
async def test_delete_swift_code(client):
    await client.post("/v1/swift-codes", json=HQ_PAYLOAD)

    del_response = await client.delete(f"/v1/swift-codes/{HQ_PAYLOAD['swiftCode']}")
    assert del_response.status_code == 200

    get_response = await client.get(f"/v1/swift-codes/{HQ_PAYLOAD['swiftCode']}")
    assert get_response.status_code == 404